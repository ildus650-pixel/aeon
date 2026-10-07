import sys

# Known stablecoins and dupes to exclude
STABLECOINS = {
    'tether', 'usdt', 'usd-coin', 'dai', 'first-digital-usd', 'usde', 'tusd',
    'usdd', 'pyusd', 'fdusd', 'paxg', 'usdc', 'usds', 'usdf', 'usds',
    'usdc', 'usdt', 'usd', 'usdcoin', 'fetusd', 'aiusd', 'bai', 'tfusd', 'xusd'
}

# Filter low volume threshold
MIN_VOLUME_USD = 1000000

# Read market data
market_data = """BTC|Bitcoin|85445|1|-0.45041|null|null|26849042443|1716918607355
ETH|Ethereum|2694.55|2|-0.69678|null|null|10952549725|329020587272
USDT|Tether|0.999934|3|-0.00084|null|null|50577972850|184069177308
BNB|BNB|778.03|4|-1.06155|null|null|680517316|103642130701
XRP|XRP|1.5|5|-0.81165|null|null|1501378841|94390349118
USDC|USDC|0.999945|6|-0.0035|null|null|15676276282|74240966708
SOL|Solana|120.4|7|-0.37144|null|null|2443637707|70848475163
TRX|TRON|0.335312|8|-0.29343|null|null|291064961|31844240995
FIGR_HELOC|Figure Heloc|1.038|9|0.52774|null|null|45693433|24450450663
ZEC|Zcash|1364.66|10|1.74051|null|null|698881361|23148091179
HYPE|Hyperliquid|91.93|11|-2.68057|null|null|928045902|20448544411
DOGE|Dogecoin|0.093622|12|-1.7508|null|null|733101637|14625544495
XMR|Monero|559.27|13|-0.31743|null|null|108074838|10521606111
LINK|Chainlink|13.94|14|0.41536|null|null|262098352|10425656674
WBT|WhiteBIT Coin|85.34|15|-0.48923|null|null|69682351|10137281263
USDS|USDS|0.999279|16|-0.0651|null|null|169358435|10131249308
ADA|Cardano|0.266714|17|-1.31382|null|null|664429185|10015366545
RAIN|Rain|0.01153865|18|1.01221|null|null|13871812|8185094790
LEO|LEO Token|8.9|19|-0.23589|null|null|151884|8185015596
XLM|Stellar|0.211689|20|-2.10339|null|null|125365513|7416723162
NEAR|NEAR Protocol|5.1|21|-4.37419|null|null|636056605|6668745989
BCH|Bitcoin Cash|311.12|22|-1.66314|null|null|160567266|6253538050
LTC|Litecoin|68.96|23|-1.23549|null|null|243250454|5357273889
UNI|Uniswap|8.5|24|-6.36348|null|null|563312382|5316020144
AVAX|Avalanche|11.55|25|3.56727|null|null|563519212|5120675358
CC|Canton|0.126247|26|0.23789|null|null|13576090|5021898703
USDE|Ethena USDe|0.999637|27|-0.00718|null|null|45499054|4984527391
SUI|Sui|1.17|28|-3.7394|null|null|507467391|4813889459
DAI|Dai|0.999867|29|-0.01097|null|null|169653574|4591361936
USD1|USD1|0.999564|30|-0.015|null|null|590603854|4442852884
HBAR|Hedera|0.099083|31|-2.58967|null|null|95375882|4359614541
GRAM|Gram (prev. Toncoin)|1.52|32|-0.21492|null|null|33298162|4285286387
QNT|Quant|264.13|33|0.37227|null|null|217309846|3840988725
TAO|Bittensor|304.88|34|0.00931|null|null|136209449|3457085107
SHIB|Shiba Inu|0.00000579|35|-1.58611|null|null|68191790|3409082961
XAUT|Tether Gold|4161.85|36|0.47774|null|null|218542975|3367302647
CRO|Cronos|0.066528|37|-4.02245|null|null|6814938|3295635898
BTW|Bitway|1.21|38|-1.28477|null|null|15925821|3288452544
ENA|Ethena|0.238613|39|-5.07259|null|null|337789236|3199491607
USDG|Global Dollar|0.999941|40|-0.00226|null|null|481677347|3184970821
PYUSD|PayPal USD|0.999743|41|-0.01947|null|null|71996587|2905911516
PUMP|Pump.fun|0.00624425|42|-2.68093|null|null|230809388|2896953820
OKB|OKB|136.47|43|4.08417|null|null|100043848|2865948664
AAVE|Aave|179.02|44|-3.81219|null|null|285906902|2763474886
RLUSD|Ripple USD|0.999907|45|-0.00962|null|null|161017960|2527185527
M|MemeCore|1.053|46|3.51461|null|null|1722190|2405275632
USYC|Circle USYC|1.14|47|0.00932|null|null|0.0|2403821598
ONDO|Ondo|0.49013|48|-1.85631|null|null|163535389|2386673255
USDY|Ondo US Dollar Yield|1.15|49|0.02355|null|null|4191463|2304333588
BUIDL|BlackRock USD Institutional Digital Liquidity Fund|1.0|50|0.0|null|null|0.0|2263137424
WLD|Worldcoin|0.549885|51|-4.73676|null|null|177103793|2090152412
SKY|Sky|0.088946|52|0.55996|null|null|22733666|2084468470
DOT|Polkadot|1.2|53|-2.1953|null|null|150104822|2039853744
ASTER|Aster|0.733326|54|-0.11269|null|null|117461689|1989670345
MNT|Mantle|0.592958|55|-9.09313|null|null|36844234|1958354995
MORPHO|Morpho|2.7|56|-0.97583|null|null|22158289|1888232265
ICP|Internet Computer|3.34|57|-6.72953|null|null|63129082|1860621660
USDF|Falcon USD|0.995955|58|-0.01008|null|null|782647|1818818297
PAXG|PAX Gold|4166.1|59|0.40663|null|null|116304251|1814107128
PEPE|Pepe|0.00000426|60|-2.57028|null|null|186698968|1793062216
WLFI|World Liberty Financial|0.056268|61|2.51541|null|null|29077077|1787885664
EURSAFO|Spiko Amundi Overnight Swap Fund (EUR)|1.14|62|0.33842|null|null|0.0|1572332401
USDD|USDD|0.999003|63|0.0428|null|null|2620671|1568817915
HTX|HTX DAO|0.00000171|64|-0.41231|null|null|50097215|1534778104
U|United Stables|0.999193|65|-0.00463|null|null|100674453|1532316489
ETC|Ethereum Classic|8.82|66|-1.72359|null|null|57401261|1398955297
BGB|Bitget Token|2.0|67|-0.2971|null|null|7636053|1398613067
ARB|Arbitrum|0.199629|68|-3.37371|null|null|143983168|1354671081
BFUSD|BFUSD|0.99978|69|-0.0002|null|null|5419479|1319657956
USDGO|USDGO|1.0|70|0.00092|null|null|21753308|1305578214
VVV|Venice Token|26.99|71|-5.71227|null|null|31251314|1302392561
KAS|Kaspa|0.04325973|72|-0.57251|null|null|11443681|1199858722
GT|Gate|11.21|73|-0.03764|null|null|726176|1172501703
JUP|Jupiter|0.351965|74|1.08983|null|null|98179406|1168266546
JST|JUST|0.141024|75|3.36247|null|null|34908522|1155078805
POL|POL (ex-MATIC)|0.107218|76|-1.77432|null|null|66149418|1139474113
RENDER|Render|2.16|77|5.32397|null|null|105992477|1122633127
ALGO|Algorand|0.123489|78|-3.5144|null|null|107327798|1119122463
KCS|KuCoin|7.66|79|0.52416|null|null|6401620|1069356040
BCAP|Blockchain Capital|108.18|80|0.0|null|null|0.0|985748168
PI|Pi Network|0.087196|81|-0.08576|null|null|3111225|980320600
FIL|Filecoin|1.15|82|-1.66558|null|null|155538276|960354996
ATOM|Cosmos Hub|1.78|83|-1.14785|null|null|41407361|953599353
LIT|Lighter|3.79|84|-4.95794|null|null|88519519|946054672
ZRO|LayerZero|2.26|85|6.08424|null|null|122715434|903316903
NEXO|NEXO|0.850241|86|-0.47335|null|null|4344997|849936417
NIGHT|Midnight|0.04977062|87|-2.43951|null|null|27342719|827246904
AERO|Aerodrome Finance|0.803217|88|-5.36084|null|null|49451117|803151714
INJ|Injective|7.96|89|3.79238|null|null|133855813|796110614
USTB|Invesco Short Duration US Government Securities Fund|11.24|90|0.0295|null|null|0.0|795116558
CAKE|PancakeSwap|2.38|91|-3.30256|null|null|56515379|759081654
ETHFI|Ether.fi|0.783396|92|4.99391|null|null|61525576|756431467
STABLE|Stable|0.02789098|93|1.20057|null|null|10295809|752482218
VET|VeChain|0.00859338|94|-2.05927|null|null|6487215|739039083
STX|Stacks|0.386703|95|2.23711|null|null|16329202|724690756
OUSD|Open USD|1.001|96|0.08337|null|null|7895.0|722144934
APT|Aptos|0.824933|97|-2.02103|null|null|82291546|718834030
DASH|Dash|55.78|98|-3.40351|null|null|85834345|717009776
GHO|GHO|0.999314|99|-0.01914|null|null|4976300|698492697
AKE|Akedo|0.02957568|100|-3.68931|null|null|6289154|674255548
"""

# Parse and filter
tokens = []
for line in market_data.strip().split('\n'):
    parts = line.split('|')
    if len(parts) >= 10:
        symbol = parts[0].lower()
        name = parts[1]
        price = float(parts[2])
        rank = int(parts[3])
        change_24h = parts[4]
        volume_usd = float(parts[7])

        # Filter out stablecoins
        if symbol in STABLECOINS or 'usd' in symbol or 'eur' in symbol or 'gbp' in symbol or 'jpy' in symbol:
            continue

        # Filter by volume
        if volume_usd < MIN_VOLUME_USD:
            continue

        # Parse 24h change
        try:
            change_24h_val = float(change_24h) if change_24h and change_24h != 'null' else None
        except:
            change_24h_val = None

        if change_24h_val is not None:
            tokens.append({
                'symbol': symbol.upper(),
                'name': name,
                'price': price,
                'rank': rank,
                'change_24h': change_24h_val,
                'volume': volume_usd,
                'market_cap': float(parts[8])
            })

# Sort by 24h change for winners/losers
tokens_sorted = sorted(tokens, key=lambda x: x['change_24h'], reverse=True)

winners = tokens_sorted[:10]
losers = tokens_sorted[-10:][::-1]  # Reverse to get lowest values

# Market pulse
top100 = tokens_sorted[:100]
positive_count = sum(1 for t in top100 if t['change_24h'] > 0)
median_change = tokens_sorted[49]['change_24h'] if len(tokens_sorted) >= 50 else None

print(f"Positive 24h in top 100: {positive_count}/100")
print(f"Median 24h change: {median_change:.2f}%" if median_change else "Median: null")
print(f"\nTop 10 Winners:")
for i, t in enumerate(winners[:10], 1):
    print(f"{i}. {t['symbol']} ({t['name']}) — ${t['price']:.2f}  +{t['change_24h']:.2f}%  •  ${t['volume']/1_000_000:.1f}M / #{t['rank']}")
print(f"\nTop 10 Losers:")
for i, t in enumerate(losers[:10], 1):
    print(f"{i}. {t['symbol']} ({t['name']}) — ${t['price']:.2f}  {t['change_24h']:.2f}%  •  ${t['volume']/1_000_000:.1f}M / #{t['rank']}")
