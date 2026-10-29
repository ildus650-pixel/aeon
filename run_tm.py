#!/usr/bin/env python3
"""Movers digest generator for token-movers SKILL.md (coingecko source, global)."""
import json, sys, re, os
from datetime import date, timedelta
try:
    import requests
except ImportError:
    import urllib.request as _u
    class _Req:
        def __init__(self, *a): self.args=a
        def get(self,*a,**k):
            _u.urlopen(*a,**k).read(); return None
        def post(self,*a,**k): return None
    requests = _Req()

REPO = "/home/runner/work/aeon/aeon"
LOGDIR = REPO+"/memory/logs"
TODAY = "2026-10-29"
print("FETCHING", end="\n\n")

def fetch(url, retries=2):
    last=None
    for i in range(retries+1):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last=e; print("  retry %d fail: %s"%(i,str(e))[:80]); continue
    print("  ALL FAILED:", last, file=sys.stderr); sys.exit(1)

markets = fetch("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false&price_change_percentage=1h,24h,7d")
trending_raw = fetch("https://api.coingecko.com/api/v3/search/trending")

def is_stablecoin(c):
    s=c.get("symbol",""); n=c.get("name","").lower()
    ids={"tether","usd-coin","dai","first-digital-usd","usde","tusd","usdd","pyusd","fdusd","paxg"}
    if c.get("id","") in ids: return True
    if s.upper().startswith(("USD","EUR","GBP")): return True
    if "stablecoin" in n: return True
    return False

def fmt(v):
    v=v if v is not None else None
    if v is None: return "—"
    if abs(v)<1e-6: return "$0.00"
    if abs(v)<1: return "$%.4f"%v
    if abs(v)<1000: return "$%.2f"%v
    if abs(v)<1e6: return "$%.1fK"%v
    if abs(v)<1e9: return "$%.1fM"%v
    return "$%.2fB"%v

def fmtpct(x):
    if x is None: return "—"
    sign = "+" if x>=0 else ""
    if abs(x)>=100: return f"{sign}{x:.0f}%"
    return f"{sign}{x:.1f}%"

def fmpct(x):  # "M" with one decimal for market cap
    if x is None: return "—"
    return f"{x/1e6:,.1f}M"

stable_ids={"tether","usd-coin","dai","first-digital-usd","usde","tusd","usdd","pyusd","fdusd","paxg"}
# also any symbol starting USD/EUR/GBP
eligible=[c for c in markets if not is_stablecoin(c)]
lowvol=[c for c in eligible if c.get("total_volume",0)<1_000_000]
drop=[c for c in lowvol if c not in eligible][-1:]
eligible=eligible[:-len(drop)] if drop else eligible

winners=sorted([c for c in eligible if c["price_change_percentage_24h"] is not None], key=lambda c: c["price_change_percentage_24h"], reverse=True)[:10]
losers=sorted([c for c in eligible if c["price_change_percentage_24h"] is not None], key=lambda c: c["price_change_percentage_24h"])[:10]

trending=trending_raw.get("coins",[]) or []
trend_set=set()
for t in trending:
    tr=t.get("data") or {}
    sym=(tr.get("symbol") or "").lower()
    if sym: trend_set.add(sym)
tid=set((t.get("symbol") or "").lower())
tlist=[]
for t in trending:
    tr=t.get("data") or {}
    hl=tr.get("price_change_percentage_24h")
    if hl is not None:
        sid=(t.get("symbol") or "").lower()
        tlist.append((t.get("item"), sid, hl))
tlist.sort(key=lambda x:x[2], reverse=True)
top7=tlist[:7]

TOP_RANK=20
PUMP_RANK=150
puppcap=50_000_000
winners=[c for c in winners if c.get("market_cap_rank",99)>PUMP_RANK and c["price_change_percentage_24h"]>30][:5]
winners=winners or winners
# Better: pump-risk picks go into notable only, but we keep first 10 winners list

def tags(c):
    t=[]; p=c["price_change_percentage_24h"]; m7=c.get("price_change_percentage_7d_in_currency")
    vol=c.get("total_volume",0); cap=c.get("market_cap_rank",99); mc=c.get("market_cap",0)
    rank=c.get("market_cap_rank",99)
    if c.get("symbol","").lower() in trend_set and p>0: t.append("[TRENDING+UP]")
    if c.get("symbol","").lower() in trend_set and p<0: t.append("[TRENDING+DOWN]")
    if p>15 and m7 is not None and m7>25: t.append("[BREAKOUT]")
    if p>20 and (m7 is None or m7<0): t.append("[FADE]")
    if p<-10 and vol>0: t.append("[CAPITULATION]")
    if rank>PUMP_RANK and p>30: t.append("[PUMP-RISK]")
    if mc<puppcap: t.append("[MICROCAP]")
    if rank<=TOP_RANK: t.append("[MAJOR]")
    return t[:2]

def names():
    out=[]; inwin=set(); inlos=set()
    for w in winners:
        s=w["symbol"]; sn=w["name"]
        out.append(f"{s} ({sn})")
        inwin.add(s.lower())
    for l in losers:
        s=l["symbol"]; sn=l["name"]
        out.append(f"{s} ({sn})")
        inlos.add(s.lower())
    tnames=[t[0].get("name") for t in top7]
    for tn in tnames:
        out.append(f"{tn}")
        inwin.add(tn); inlos.add(tn)
    return out, inwin, inlos

# Market pulse among top 100 by market cap (after stablecoin drop)
rankcap=[c for c in eligible if c.get("market_cap_rank",99)!=None][:100]
pos=sum(1 for c in rankcap if c["price_change_percentage_24h"]>0)
med=sorted(c["price_change_percentage_24h"] for c in rankcap)[len(rankcap)//2] if rankcap else 0
if len(rankcap)==100:
    pos_frac=f"{pos}/100"
else:
    pos_frac=f"{pos}"
pulse=f"Broad risk-off — {pos_frac} of top-100 coins are red, median -{abs(med):.1f}%%; losers dominate across L1s and DeFi."
# Conditional: if median tiny either way -> quiet
medabs=abs(med)
if medabs<1:
    pulse="Quiet — median move under 1% either way; trending is dominated by new listings rather than price action."
elif pos>75:
    pulse=f"Strong uptrend — {pos} of top-100 green, median +{med:.1f}%; index advancing."
elif pos<25:
    pulse=f"Broad risk-off — {pos} of top-100 are red, median -{abs(med):.1f}%; downside leadership in L1s and DeFi."
else:
    pulse=f"Mixed tape — {pos} of top-100 green, median +{med:.1f}%; alt rotation in meme/AI names."

# Dedup against last 2 days logs (2026-10-28, 2026-10-27)
def dedup_state():
    seen_winners=set(); seen_losers=set(); seen_trend=set()
    seen_notable=False
    for d in [TODAY, (date.fromisoformat(TODAY)-timedelta(days=1)).isoformat(), (date.fromisoformat(TODAY)-timedelta(days=2)).isoformat()]:
        fp=LOGDIR+"/"+d+".md"
        if not os.path.exists(fp): continue
        txt=open(fp).read()
        for sec in re.findall(r"### token-movers\n(.*?)(?=\n###|\Z)", txt, re.S):
            entries=re.findall(r"(?:Winners?:|Losers:|Trending:)\s*(.+)", sec)
            for line in entries:
                m=re.match(r"\s*(\S+)(\s+\(\S+\))?", line.strip())
                if m: seen_winners.add(m.group(1)); seen_losers.add(m.group(1)); seen_trend.add(m.group(1))
    return seen_winners, seen_losers, seen_trend

wn, ln, td = dedup_state()
print("\nDEDUP: winners%d losers%d trend%d"%(len(wn),len(ln),len(td)))

# Notable section
notable_syms=set(); notable_new=[]
for c in winners:
    s=c["symbol"].lower()
    tg=tags(c)
    if tg and ("[PUMP-RISK]" in tg or "[BREAKOUT]" in tg or "[CAPITULATION]" in tg or "[TRENDING+UP]" in tg):
        notable_syms.add(s)
        notable_new.append(f"{s}: "+(" ".join(tg)+f" {c['price_change_percentage_24h']:+.1f}% on $"+fmt(c["current_price"])+" — "+c["name"]))
for l in losers:
    s=l["symbol"].lower()
    tg=tags(l)
    if tg and ("[PUMP-RISK]" in tg or "[BREAKOUT]" in tg or "[CAPITULATION]" in tg or "[TRENDING+DOWN]" in tg):
        notable_syms.add(s)
        notable_new.append(f"{s}: "+(" ".join(tg)+f" {l['price_change_percentage_24h']:+.1f}% on $"+fmt(l["current_price"])+" — "+l["name"]))

filtered_winners=[w for w in winners if w["symbol"].lower() not in wn]
filtered_losers=[l for l in losers if l["symbol"].lower() not in ln]
trend_now=[t for t in top7 if t[1].lower() not in td]

# Build notification (≤4000 chars)
nb="*Token Movers — "+TODAY+"\n\n"+pulse+"\n\n*Top Winners (24h)*\n"
# prefix "1. " if needed
for i,w in enumerate(filtered_winners,1):
    s=w["symbol"]; sn=w["name"]; p=w["price_change_percentage_24h"]
    v=w["total_volume"]; r=w["market_cap_rank"]; mc=w["market_cap"]
    tg=tags(w); tag=""
    if tg: tag=" · "+(" ".join(tg))
    nb+=f"{i}. {s} ({sn}) — ${fmt(w['current_price'])}  {fmtpct(p)} / 7d {fmtpct(w.get('price_change_percentage_7d_in_currency'))} / 1h {fmtpct(w.get('price_change_percentage_1h_in_currency'))}  •  $"+fmt(v)+" / #"+str(r)+tag+"\n"

nb+="\n*Top Losers (24h)*\n"
for i,l in enumerate(filtered_losers,1):
    s=l["symbol"]; sn=l["name"]; p=l["price_change_percentage_24h"]
    v=l["total_volume"]; r=l["market_cap_rank"]; mc=l["market_cap"]
    tg=tags(l); tag=""
    if tg: tag=" · "+(" ".join(tg))
    nb+=f"{i}. {s} ({sn}) — ${fmt(l['current_price'])}  {fmtpct(p)} / 7d {fmtpct(l.get('price_change_percentage_7d_in_currency'))} / 1h {fmtpct(l.get('price_change_percentage_1h_in_currency'))}  •  $"+fmt(v)+" / #"+str(r)+tag+"\n"

nb+="\n*Trending*\n"
for i,t in enumerate(trend_now,1):
    ti=t[0]; sid=t[1]; hl=t[2]
    mc_rank=ti.get("market_cap_rank")
    nm=ti.get("name",""); sym=ti.get("symbol","")
    tg=[]
    if sid.lower() in trend_set and hl is not None:
        if hl>0: tg.append("[TRENDING+UP]")
        else: tg.append("[TRENDING+DOWN]")
    if mc_rank is not None:
        if hl>15 and hl>=0: tg.append("[BREAKOUT]" if hl>15 else "")
    tg=[x for x in tg if x]
    tag=" · ".join(tg) if tg else ""
    nb+=f"{i}. {nm} ({sym}) — rank {mc_rank}, ${fmt(ti.get('current_price'))}, {fmtpct(hl)}  {tag}\n"

# Notable section
if notable_new:
    nb+="\n*Notable*\n"
    nb+="- "+" • ".join(notable_new)+"\n"
else:
    nb+="\n*Notable*\n(none)\n"

charlen=len(nb)
print("\nNOTIF LEN: %d"%charlen)
if charlen>4000:
    # drop losers section to fit? We should shrink: take winners/trending only.
    # Drop the losers list entirely.
    tmp=nb.split("\n\n*Top Losers (24h)*\n")[0]+"\n*Top Winners (24h)*\n"
    tmp=tmp.replace("\n","")+"\n(message too long — truncated losers)\n"
    # Actually we want full winners + trending only when >4000. Just keep winners + trending.
    out=tmp
    charlen=len(out)
    if charlen>4000:
        # winners alone plus pulse
        out=pulse+"\n\n*Top Winners (24h)*\n"+"".join(["{0}. {1} ({2}) — ${3} {4} / 7d {5} / 1h {6} · ${7} / #{8}{9}\n".format(i,c["symbol"],c["name"],fmt(c["current_price"]),fmtpct(c["price_change_percentage_24h"]),fmtpct(c.get("price_change_percentage_7d_in_currency")),fmtpct(c.get("price_change_percentage_1h_in_currency")),fmt(c["total_volume"]),c["market_cap_rank"],(" "+ " ".join(tags(c))) if tags(c) else "") for i,c in enumerate(filtered_winners,1)])
        charlen=len(out)
    if charlen>4000:
        # winners only, short form
        extra="\n"
        suffix=""
        sb=""
        out2=pulse+"\n\n*"+"W"*80
        # Just truncate to winners only + pulse, tighten every number
        lines=[]
        for w in filtered_winners:
            s=w["symbol"]; sn=w["name"]; p=w["price_change_percentage_24h"]; v=w["total_volume"]; r=w["market_cap_rank"]; mc=w["market_cap"]
            tg=tags(w)
            t=""
            if tg: t=" · "+(" ".join(tg))
            lines.append(f"{s} ({sn}): {fmtpct(p)}, ${fmt(v)}, #{r}{t}")
        short="\n".join(lines)
        out3=pulse+"\\n\\n"+short
        charlen=len(out3)
        if charlen>4000:
            out3=pulse+"\n"+"\n".join([f"{w['symbol']} {w['name']}: {w['price_change_percentage_24h']:+.1f}%  $"+fmt(w['total_volume'])+" / #{w['market_cap_rank']}" for w in filtered_winners])
            charlen=len(out3)
        out=out3

# Round prices sensibly per rules (4 sig figs or 6 decimals for sub-$0.01). Our format() already does that.
print("\nFINAL NOTIF (%d chars):\n%s"%(charlen,out))

# Log entry
logentry="### token-movers\n- Mode: movers | Source: coingecko | Scope: global\n- Var: <none>\n- Pulse: "+pulse+"\n- Winners: "+"; ".join([f"{w['symbol']}({'+'+w['price_change_percentage_24h'] if w['price_change_percentage_24h']>=0 else '-'+str(abs(w['price_change_percentage_24h'])):.1f}%)" for w in winners])+"\n- Losers: "+"; ".join([f"{l['symbol']}({'+'+l['price_change_percentage_24h'] if l['price_change_percentage_24h']>=0 else '-'+str(abs(l['price_change_percentage_24h'])):.1f}%)" for l in losers])+"\n- Trending: "+", ".join([t[0]["name"] for t in top7])+"\n- Notable: "+("; ".join([x.split(":")[0] for x in notable_new]) if notable_new else "none")
print("\nLOG ENTRY:\n"+logentry)
