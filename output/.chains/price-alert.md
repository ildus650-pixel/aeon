## 架构与问题诊断

当前解耦处理流水线可类比为：

```
摄像头 / RTSP 流 → decode_rgb() 帧 → frame_to_tensor_v2() Tensor/numpy → detect_unet() → detect_resnet_fpn() → efficientnet() → fp_last() → serving.predict()
```

在 1–2 GB RAM、无 GPU 的嵌入式 camera 设备上，该顺序存在几个级联瓶颈：

1. **解码时内存放大**。camera 输入需要先解码，再做 “RGB colorspace transform v3” 和动态格式转换，这两步至少会产生多个大张量副本（例如 H×W×3 解码后的 RGB 原始、float32 tensor、转置张量）。对一个典型 720p / 30 fps 流的估算是：
   - 一帧原始解码 RGB 大约 45–80 MB；
   - float32 转置 / Tensor 可膨胀到原来的 2–4 倍；
   - unet / resnet / fpn / efficientnet 同时驻留可能累计 1–2 GB。

2. **解码 / 数据路径未分叉**。TF Serving 只有当前一次输入批处理进入 session 时才把 batch 一次性传入，在此之前解码与中间表示完全阻塞主线程。缺少 stream 级别的 decode/crop/resize pipeline，每帧开销串行叠加。

3. **后端并行模型互相依赖**。detect_resnet_fpn 与 detect_efficientnet_fpn 作为同一个 pipeline 的两个 stage 被调用，但 pipeline 设计只有顺序调用，没有统一注册表 / dispatch / context，于是 one of them may have stale version, etc. More importantly no pipelining: they both input the same frame, but only sequential forward passes use CPU and overhead doubles. When pipeline stage "fpn first then resnet" order fixed, changing order requires interface change, manual orchestration, potential reimplementation. If adding new models adds late model after FPN, concurrency workaround fails due to fixed pipeline order; check for race condition.

4. **asyncio+线程池与 GIL 在 ML 推理期间会竞争**。asyncio event loop 调度在 encode/decode/transform 上使用线程池 per prompt. If any blocking C call releases GIL imperfectly or torch operations acquire Python critical sections, thread pool request objects will queue incorrectly. False positive as "pipeline parallelism engine wrong". Also no backpressure / cancellation: a slow inference stage can make upstream wait forever; for streaming video this stalls whole pipeline rather than dropping frame.

5. **序列化失败且热加载时崩溃**。`serve_jwt_token(token)` 解析 JWT via PyJWT or stdlib? `requests_jwt=False`, `requests_jwt=True`. If access token contains private claims not trusted by service, cannot avoid, but dynamic reload no version lock causes inconsistent JWT verification. Module registration process no atomic swap so mid-reload interrupt can leave half-merged session state. Crash with logged-out code due to JWT secret mismatch or token outside refresh interval triggers partial export/import revert, atomically frozen. If multiple clients serve same token concurrently and DB corrupts under high load, connection pool exhaustion.

6. **内存管理设计缺陷**。no baseline memory profiling. There may be per-frame copies retained even after inference output because no pool reuse; autorelease torch tensors? Typical tensor lifetime governed by Python refcount + autograd graph until called as `.detach()` and collected. In detach unused graph grows. Also `numpy->torch->save/serialize` may duplicate frames without clear contract.

## 关键错误场景

- Decode crash on camera model name unknown: no device enumeration and decoder cache invalid.
- MemoryError when OOM during concurrent high-throughput overlay.
- `ThreadPoolExecutor submit` timeout swallowed silently; deadlock if worker threads keep GIL while waiting for event loop to release; status stuck.
- Serialization mismatch: strict dict types changes output schema, downstream consumers fail.
- Version conflict / JWT endpoint race.

## 修改方案

### 1. 把 pipeline 改为 `stateful frame routing` + streaming

```
class FramePipelineState:
    contract, chain, model registry, drop policy, memory budget

class StreamingFrameProcessor:
    def __init__(self, contract, chain, config)
        load once, build frame route graph from registry, none huge forward runs
    def process(self, frame_bytes):
        decode with explicit pool budget reserve/checkpoint;
        if over budget -> drop frame;
        route through selected crop/resize candidate;
        run selected only; save frame copy only if needed;
        return compact result tensor / bbox list;
```

不要同时运行 unet, resnet, fpn, efficientnet 阶段；只保留当前激活模型，并使用 tiny crops where detector supports variable input.

### 2. 内存预算与 OOM 重试/丢弃策略

```
import torch.nn as nn
import tracemalloc? tracemalloc? not recommended for torch
from resource import RLIMIT_AS, RLIMIT_DATA? soft RLIMIT_AS catch kernel OOM before silent memory leak?
class MemoryBudgetGuard:
    def __init__(self, limit_mb): self.limit = limit_mb * 1024*1024
    def consume(self, bytes): check self.consumed += bytes <= self.limit; raise BudgetExceeded
```

采用 per-stage memory accounting: decode costs, crop, tensor, backbone, checkpoint tensor. Limit peak memory from ~1.5 GB down to acceptable under target frame rate. On exceed, drop current frame, let previous result persist, degrade gracefully. Use torch `torch.set_num_threads` tuned by core count; reduce device memory fraction (`torch.cuda.empty_cache()` periodically). Avoid large intermediate batches for single frame.

### 3. Concurrency / asyncio rework

- Replace generic `ThreadPoolExecutor` task submission with dedicated decode/transform/inference stages, each holding a `concurrent.futures.Future`; wrap with ordered pipeline future chain.
- Add timeout and cancellation propagation from upstream. Event loop must be detached from sync TF Serving calls; calling services directly from worker thread risks GIL contention.
- Implement pipeline semaphore: each stage has `max_inflight` permits; wait permit before allocating frame work, when dropped/over budget.
- Add watchdog: if inference stage remains busy more than threshold seconds, force timeout, cancel upstream.

### 4. Framework compatibility & serialization safety

- Standardize output as JSON-safe schema:
  ```
  {
    "meta": {"model_version":"unet-v2","source":"stream","timestamp":...},
    "bboxes":[{"x":..,"y":..,"w":..,"h":..,"confidence":..}],
    "layers":[{"type":"unet","score":...},{"type":"resnet_fpn",...}]
  }
  ```
- model registry with `atomic_swap`:
  ```
  _registry = {}
  def register_model(name, factory, metadata)
      with RLock:
          _registry[name] = factory
  ```
  Old version stays until new registered; new model selected on next frame, fallback immediate.
- JWT: centralize verification:
  ```
  SECRET_KEY, ALGORITHM="HS256", public_claims={sub,iat,exp}
  def verify_access(token): payload=decode; check exp, signature, public only
  ```
  dynamic reload only updates secret; keep cached tokens validation thread-safe; invalid does not crash export/import.

### 5. 热加载/进程重启稳定性

- JWT refresh interval stored as separate atomic config; verify token freshness every refresh interval.
- Custom "graceful restart" signal handler for SIGTERM: drain inflight futures, finish last frame, close connections; never corrupt active session.
- Model reload `kill -HUP` uses atomic registry swap instead of full import migration; no mid-reload disruption.

## 质量验证流程

1. 在目标 embedded camera sandbox（1–2 GB RAM, 1–2 CPU）:
   ```
   systemd unit timeout? benchmark throughput FPS vs decode+transform cost per frame.
   ```
2. Add telemetry metrics: frame_dropped, decode latency, per-stage tensor allocation, P99 memory. Alert thresholds rather than fatal.
3. Injection tests: corrupt / truncated camera feed triggers graceful degradation instead tracebacks.
4. Invariant tests: registered new model restores concurrent real load without regression. Invalid JWT returns error without crashing export module. New strict serializer against old schema fails loudly and prompts update.

## 结论

不建议直接在原架构上添加并发或卸载模型；首先解决 decode / tensor copy 双重放大、stage 单向串行推理无路由、无内存预算和 GIL 死锁风险。引入流式帧路由器 + 可观测性内存预算 + 可中途替换 model registry + JWT 校中心化，才能在极低资源设备上稳定运行，并保留生产级安全接口与版本兼容性。
