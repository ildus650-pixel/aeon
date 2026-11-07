#!/usr/bin/env python3
import json

# Data from the curl response
data = """[{"id":"bitcoin","symbol":"btc","name":"Bitcoin","image":"https://coin-images.coingecko.com/coins/images/1/large/bitcoin.png?1696501400","current_price":75658,"market_cap":1521401794114,"market_cap_rank":1,"fully_diluted_valuation":1521406333553,"total_volume":15732869799,"high_24h":76150,"low_24h":75352,"price_change_24h":73.88,"price_change_percentage_24h":0.05581,"market_cap_change_24h":1752617173,"market_cap_change_percentage_24h":0.11533,"circulating_supply":20109115.0,"total_supply":20109175.0,"max_supply":21000000.0,"ath":126080,"ath_change_percentage":-39.9919,"ath_date":"2025-10-06T10:57:42.000Z","atl":67.81,"atl_change_percentage":111475.37528,"atl_date":"2013-07-05T16:00:00.000Z","roi":null,"last_updated":"2026-11-07T15:47:55.000Z","price_change_percentage_1h_in_currency":0.0191,"price_change_percentage_24h_in_currency":0.05581,"price_change_percentage_7d_in_currency":-2.0244},{"id":"ethereum","symbol":"eth","name":"Ethereum","image":"https://coin-images.coingecko.com/coins/images/279/large/ethereum.png?1696501628","current_price":2233.7,"market_cap":272934437815,"market_cap_rank":2,"fully_diluted_valuation":272934437815,"total_volume":5528680427,"high_24h":2248.6,"low_24h":2216.76,"price_change_24h":10.93,"price_change_percentage_24h":0.44696,"market_cap_change_24h":1323488657,"market_cap_change_percentage_24h":0.48727,"circulating_supply":122197894.00927158,"total_supply":122197894.00927158,"max_supply":null,"ath":4946.05,"ath_change_percentage":-54.83868,"ath_date":"2025-08-24T11:21:03.000Z","atl":0.432979,"atl_change_percentage":515791.39979,"atl_date":"2015-10-19T16:00:00.000Z","roi":{"times":43.309089628863546,"currency":"btc","percentage":4330.908962886355},"last_updated":"2026-11-07T15:47:55.000Z","price_change_percentage_1h_in_currency":0.0487,"price_change_percentage_24h_in_currency":0.44696,"price_change_percentage_7d_in_currency":-0.2291},{"id":"tether","symbol":"usdt","name":"Tether","image":"https://coin-images.coingecko.com/coins/images/325/large/Tether.png?1696501661","current_price":0.999225,"market_cap":176890580158,"market_cap_rank":3,"fully_diluted_valuation":182353283750,"total_volume":26154635861,"high_24h":0.99927,"low_24h":0.998901,"price_change_24h":0.00019396,"price_change_percentage_24h":0.01926,"market_cap_change_24h":-684222101.3024902,"market_cap_change_percentage_24h":-0.38531,"circulating_supply":177028037577.4114,"total_supply":182494986105.0762,"max_supply":null,"ath":1.32,"ath_change_percentage":-24.47819,"ath_date":"2018-07-23T16:00:00.000Z","atl":0.572521,"atl_change_percentage":74.5308,"atl_date":"2015-03-01T16:00:00.000Z","roi":null,"last_updated":"2026-11-07T15:47:55.000Z","price_change_percentage_1h_in_currency":-0.0013,"price_change_percentage_24h_in_currency":0.01926,"price_change_percentage_7d_in_currency":-0.0081},{"id":"binancecoin","symbol":"bnb","name":"BNB","image":"https://coin-images.coingecko.com/coins/images/825/large/bnb-icon2_2x.png?1696501970","current_price":693.18,"market_cap":91159548149,"market_cap_rank":4,"fully_diluted_valuation":91159548149,"total_volume":614597299,"high_24h":696.94,"low_24h":691.4,"price_change_24h":-1.6678283908977392,"price_change_percentage_24h":-0.26337,"market_cap_change_24h":-220156484.22209167,"market_cap_change_percentage_24h":-0.24092,"circulating_supply":131511042.33,"total_supply":131511042.33,"max_supply":200000000.0,"ath":1369.99,"ath_change_percentage":-49.40288,"ath_date":"2025-10-13T00:41:24.000Z","atl":0.0398177,"atl_change_percentage":1740774.87928,"atl_date":"2017-10-18T16:00:00.000Z","roi":null,"last_updated":"2026-11-07T15:47:55.000Z","price_change_percentage_1h_in_currency":-0.1053,"price_change_percentage_24h_in_currency":-0.26337,"price_change_percentage_7d_in_currency":-1.3584},{"id":"ripple","symbol":"xrp","name":"XRP","image":"https://coin-images.coingecko.com/coins/images/44/large/xrp-symbol-white-128.png?1696501442","current_price":1.15,"market_cap":73289051444,"market_cap_rank":5,"fully_diluted_valuation":115369017753,"total_volume":1594373948,"high_24h":1.2,"low_24h":1.15,"price_change_24h":-0.029530716213584496,"price_change_percentage_24h":-2.50607,"market_cap_change_24h":-1884461561.8752441,"market_cap_change_percentage_24h":-2.50682,"circulating_supply":63516606953.0,"total_supply":99985583260.0,"max_supply":100000000000.0,"ath":3.65,"ath_change_percentage":-68.3523,"ath_date":"2025-07-17T19:40:53.000Z","atl":0.00268621,"atl_change_percentage":42860.00851,"atl_date":"2014-05-21T16:00:00.000Z","roi":null,"last_updated":"2026-11-07T15:47:55.000Z","price_change_percentage_1h_in_currency":0.1076,"price_change_percentage_24h_in_currency":-2.50607,"price_change_percentage_7d_in_currency":-6.4771},{"id":"usd-coin","symbol":"usdc","name":"USDC","image":"https://coin-images.coingecko.com/coins/images/6319/large/USDC.png?1769615602","current_price":0.999725,"market_cap":70512729840,"market_cap_rank":6,"fully_diluted_valuation":70522114255,"total_volume":6844388991,"high_24h":0.999931,"low_24h":0.999437,"price_change_24h":0.0002269,"price_change_percentage_24h":0.02267,"market_cap_change_24h":219318492,"market_cap_change_percentage_24h":0.312,"circulating_supply":70532248542.43767,"total_supply":70541635554.9752,"max_supply":null,"ath":1.043,"ath_change_percentage":-4.19181,"ath_date":"2018-11-14T16:00:00.000Z","atl":0.877647,"atl_change_percentage":13.90969,"atl_date":"2023-03-11T00:02:13.000Z","roi":null,"last_updated":"2026-11-07T15:47:55.000Z","price_change_percentage_1h_in_currency":0.0,"price_change_percentage_24h_in_currency":0.02267,"price_change_percentage_7d_in_currency":-0.0235},{"id":"solana","symbol":"sol","name":"Solana","image":"https://coin-images.coingecko.com/coins/images/4128/large/solana.png?1718769756","current_price":89.25,"market_cap":52734869963,"market_cap_rank":7,"fully_diluted_valuation":56852514146,"total_volume":1168612371,"high_24h":90.65,"low_24h":89.59,"price_change_24h":-0.9828726087668542,"price_change_percentage_24h":-1.13603,"market_cap_change_24h":-530686876.2804413,"market_cap_change_percentage_24h":-0.9963,"circulating_supply":590982483.1699408,"total_supply":637127578.165966,"max_supply":null,"ath":293.31,"ath_change_percentage":-69.57322,"ath_date":"2025-01-19T03:15:27.000Z","atl":0.500801,"atl_change_percentage":17720.52217,"atl_date":"2020-05-11T11:35:23.000Z","roi":null,"last_updated":"2026-11-07T15:47:55.000Z","price_change_percentage_1h_in_currency":-0.0481,"price_change_percentage_24h_in_currency":-1.13603,"price_change_percentage_7d_in_currency":-6.0911},{"id":"tron","symbol":"trx","name":"TRON","image":"https://coin-images.coingecko.com/coins/images/1094/large/photo_2026-04-13_09-59-16.png?1776048311","current_price":0.319433,"market_cap":30353679644,"market_cap_rank":8,"fully_diluted_valuation":30353732470,"total_volume":327661070,"high_24h":0.319797,"low_24h":0.317045,"price_change_24h":0.0013037,"price_change_percentage_24h":0.39805,"market_cap_change_24h":122719372,"market_cap_change_percentage_24h":0.40594,"circulating_supply":95028939715.00452,"total_supply":95029105098.5738,"max_supply":null,"ath":0.431288,"ath_change_percentage":-25.9352,"ath_date":"2024-12-03T16:10:40.000Z","atl":0.00180434,"atl_change_percentage":17603.56771,"atl_date":"2017-11-11T16:00:00.000Z","roi":{"times":175.85388089843906,"currency":"usd","percentage":17585.388089843906},"last_updated":"2026-11-07T15:47:55.000Z","price_change_percentage_1h_in_currency":-0.0606,"price_change_percentage_24h_in_currency":0.39805,"price_change_percentage_7d_in_currency":0.5139},{"id":"figure-heloc","symbol":"figr_heloc","name":"Figure Heloc","image":"https://coin-images.coingecko.com/coins/images/68480/large/figure.png?1755863954","current_price":1.022,"market_cap":26948393963,"market_cap_rank":9,"fully_diluted_valuation":26948393963,"total_volume":32971196,"high_24h":1.04,"low_24h":1.02,"price_change_24h":-0.013255071317254341,"price_change_percentage_24h":-1.28026,"market_cap_change_24h":-229804290.82422256,"market_cap_change_percentage_24h":-0.84555,"circulating_supply":26370458025.989,"total_supply":26370458025.989,"max_supply":null,"ath":1.076,"ath_change_percentage":-4.99642,"ath_date":"2026-11-01T13:20:30.000Z","atl":0.155357,"atl_change_percentage":557.7868,"atl_date":"2025-10-31T06:27:24.000Z","roi":null,"last_updated":"2026-11-07T15:47:55.000Z","price_change_percentage_1h_in_currency":-0.006,"price_change_percentage_24h_in_currency":-1.28026,"price_change_percentage_7d_in_currency":-0.5216},{"id":"zcash","symbol":"zec","name":"Zcash","image":"https://coin-images.coingecko.com/coins/images/486/large/Brandmark-Yellow_%281%29.png?1785810558","current_price":1252.2,"market_cap":21315413865,"market_cap_rank":10,"fully_diluted_valuation":21315759932,"total_volume":847626676,"high_24h":1372.78,"low_24h":1265.21,"price_change_24h":-85.69016978968875,"price_change_percentage_24h":-6.57727,"market_cap_change_24h":-1462807466.162796,"market_cap_change_percentage_24h":-6.42196,"circulating_supply":17028538.96477089,"total_supply":17028815.43201981,"max_supply":21000000.0,"ath":3191.93,"ath_change_percentage":-60.76982,"ath_date":"2016-10-28T16:00:00.000Z","atl":16.08,"atl_change_percentage":7687.24786,"atl_date":"2024-07-04T20:22:29.000Z","roi":null,"last_updated":"2026-11-07T15:47:55.000Z","price_change_percentage_1h_in_currency":-0.1274,"price_change_percentage_24h_in_currency":-6.57727,"price_change_percentage_7d_in_currency":-1.2272},{"id":"hyperliquid","symbol":"hype","name":"Hyperliquid","image":"https://coin-images.coingecko.com/coins/images/50882/large/hyperliquid.jpg?1729431300","current_price":77.33,"market_cap":18511226241,"market_cap_rank":11,"fully_diluted_valuation":73574097267,"total_volume":637932724,"high_24h":79.58,"low_24h":77.4,"price_change_24h":-0.7416967609218261,"price_change_percentage_24h":-0.94477,"market_cap_change_24h":-180511851.10964584,"market_cap_change_percentage_24h":-0.96573,"circulating_supply":239406814.37414145,"total_supply":951538272.9141414,"max_supply":1000000000.0,"ath":97.96,"ath_change_percentage":-21.05835,"ath_date":"2026-09-23T05:16:50.000Z","atl":3.81,"atl_change_percentage":1930.42289,"atl_date":"2024-11-29T01:30:30.000Z","roi":null,"last_updated":"2026-11-07T15:47:55.000Z","price_change_percentage_1h_in_currency":-0.1404,"price_change_percentage_24h_in_currency":-0.94477,"price_change_percentage_7d_in_currency":-10.4459},{"id":"monero","symbol":"xmr","name":"Monero","image":"https://coin-images.coingecko.com/coins/images/69/large/monero_logo.png?1696501460","current_price":613.19,"market_cap":11549011336,"market_cap_rank":12,"fully_diluted_valuation":11549011336,"total_volume":82175066,"high_24h":624.26,"low_24h":603.55,"price_change_24h":-9.315876103287337,"price_change_percentage_24h":-1.39809,"market_cap_change_24h":-171225564.19140244,"market_cap_change_percentage_24h":-1.46094,"circulating_supply":18827919.918684524,"total_supply":18827919.918684524,"max_supply":null,"ath":797.73,"ath_change_percentage":-23.13336,"ath_date":"2026-01-14T11:34:07.000Z","atl":0.216177,"atl_change_percentage":283553.13377,"atl_date":"2015-01-13T16:00:00.000Z","roi":null,"last_updated":"2026-11-07T15:47:55.000Z","price_change_percentage_1h_in_currency":0.2902,"price_change_percentage_24h_in_currency":-1.39809,"price_change_percentage_7d_in_currency":3.6846},{"id":"dogecoin","symbol":"doge","name":"Dogecoin","image":"https://coin-images.coingecko.com/coins/images/5/large/dogecoin.png?1696501409","current_price":0.071484,"market_cap":11196599186,"market_cap_rank":13,"fully_diluted_valuation":11196750715,"total_volume":224361983,"high_24h":0.073116,"low_24h":0.071646,"price_change_24h":-0.001193524865608683,"price_change_percentage_24h":-1.65885,"market_cap_change_24h":-186836279.08558846,"market_cap_change_percentage_24h":-1.6413,"circulating_supply":156648462860.16907,"total_supply":156650582860.16907,"max_supply":null,"ath":0.731578,"ath_change_percentage":-90.22876,"ath_date":"2021-05-07T21:08:23.000Z","atl":8.69e-05,"atl_change_percentage":82156.84597,"atl_date":"2015-05-05T16:00:00.000Z","roi":null,"last_updated":"2026-11-07T15:47:55.000Z","price_change_percentage_1h_in_currency":-0.0178,"price_change_percentage_24h_in_currency":-1.65885,"price_change_percentage_7d_in_currency":-4.6387},{"id":"usds","symbol":"usds","name":"USDS","image":"https://coin-images.coingecko.com/coins/images/39926/large/usds.webp?1726666683","current_price":1.0,"market_cap":8788847415,"market_cap_rank":14,"fully_diluted_valuation":8788847415,"total_volume":177476328,"high_24h":1.001,"low_24h":0.999535,"price_change_24h":0.00018641,"price_change_percentage_24h":0.00864,"market_cap_change_24h":-724838448.1501503,"market_cap_change_percentage_24h":-7.6189,"circulating_supply":8787040661.534924,"total_supply":8787040661.534924,"max_supply":null,"ath":1.057,"ath_change_percentage":-5.39256,"ath_date":"2024-10-28T21:40:51.000Z","atl":0.948265,"atl_change_percentage":5.48795,"atl_date":"2024-10-03T05:19:28.000Z","roi":null,"last_updated":"2026-11-07T15:47:55.000Z","price_change_percentage_1h_in_currency":0.0089,"price_change_percentage_24h_in_currency":0.00864,"price_change_percentage_7d_in_currency":-0.0162},{"id":"whitebit","symbol":"wbt","name":"WhiteBIT Coin","image":"https://coin-images.coingecko.com/coins/images/27045/large/wbt_token.png?1696526096","current_price":72.7,"market_cap":8625436653,"market_cap_rank":15,"fully_diluted_valuation":21315200942,"total_volume":54508096,"high_24h":73.19,"low_24h":72.35,"price_change_24h":0.142619,"price_change_percentage_24h":0.10383,"market_cap_change_24h":15409265,"market_cap_change_percentage_24h":0.17897,"circulating_supply":118657693.0,"total_supply":293227192.0,"max_supply":400000000.0,"ath":87.91,"ath_change_percentage":-17.29969,"ath_date":"2026-09-21T20:29:10.000Z","atl":3.06,"atl_change_percentage":2274.64896,"atl_date":"2023-02-13T11:01:21.000Z","roi":null,"last_updated":"2026-11-07T15:47:55.000Z","price_change_percentage_1h_in_currency":0.0114,"price_change_percentage_24h_in_currency":0.10383,"price_change_percentage_7d_in_currency":-1.8572},{"id":"leo-token","symbol":"leo","name":"LEO Token","image":"https://coin-images.coingecko.com/coins/images/8418/large/leo-token.png?1696508607","current_price":9.33,"market_cap":8582899845,"market_cap_rank":16,"fully_diluted_valuation":9192955160,"total_volume":162178,"high_24h":9.39,"low_24h":9.26,"price_change_24h":0.00010364,"price_change_percentage_24h":0.00179,"market_cap_change_24h":88428,"market_cap_change_percentage_24h":0.00103,"circulating_supply":919857851.9,"total_supply":985239504.0,"max_supply":null,"ath":10.61,"ath_change_percentage":-12.08415,"ath_date":"2026-05-04T09:35:00.000Z","atl":0.799859,"atl_change_percentage":1066.54136,"atl_date":"2019-12-24T07:14:35.000Z","roi":null,"last_updated":"2026-11-07T15:47:55.000Z","price_change_percentage_1h_in_currency":-0.0385,"price_change_percentage_24h_in_currency":0.00179,"price_change_percentage_7d_in_currency":-0.4326},{"id":"chainlink","symbol":"link","name":"Chainlink","image":"https://coin-images.coingecko.com/coins/images/877/large/Chainlink_Logo_500.png?1760023405","current_price":10.82,"market_cap":8296574792,"market_cap_rank":17,"fully_diluted_valuation":10819032551,"total_volume":185644702,"high_24h":10.96,"low_24h":10.73,"price_change_24h":-0.09116394583834442,"price_change_percentage_24h":-0.85022,"market_cap_change_24h":-70388893.17586517,"market_cap_change_percentage_24h":-0.84127,"circulating_supply":766849970.424884,"total_supply":1000000000.0,"max_supply":1000000000.0,"ath":52.7,"ath_change_percentage":-79.46793,"ath_date":"2021-05-09T16:13:57.000Z","atl":0.148183,"atl_change_percentage":7201.57111,"atl_date":"2017-11-28T16:00:00.000Z","roi":null,"last_updated":"2026-11-07T15:47:55.000Z","price_change_percentage_1h_in_currency":0.3233,"price_change_percentage_24h_in_currency":-0.85022,"price_change_percentage_7d_in_currency":-5.6265},{"id":"cardano","symbol":"ada","name":"Cardano","image":"https://coin-images.coingecko.com/coins/images/975/large/cardano.png?1696502090","current_price":0.18175,"market_cap":6819469150,"market_cap_rank":18,"fully_diluted_valuation":8165118168,"total_volume":132026480,"high_24h":0.188427,"low_24h":0.182135,"price_change_24h":-0.005622058830057092,"price_change_percentage_24h":-3.0446,"market_cap_change_24h":-212144334.53504562,"market_cap_change_percentage_24h":-3.01701,"circulating_supply":37583793088.09034,"total_supply":45000000000.0,"max_supply":45000000000.0,"ath":3.09,"ath_change_percentage":-94.12132,"ath_date":"2021-09-01T22:00:10.000Z","atl":0.01925275,"atl_change_percentage":842.56462,"atl_date":"2020-03-12T18:22:55.000Z","roi":null,"last_updated":"2026-11-07T15:47:55.000Z","price_change_percentage_1h_in_currency":0.0129,"price_change_percentage_24h_in_currency":-3.0446,"price_change_percentage_7d_in_currency":-5.0318},{"id":"stellar","symbol":"xlm","name":"Stellar","image":"https://coin-images.coingecko.com/coins/images/100/large/fmpFRHHQ_400x400.jpg?1735231350","current_price":0.151242,"market_cap":5349984439,"market_cap_rank":19,"fully_diluted_valuation":7562581290,"total_volume":92180796,"high_24h":0.157318,"low_24h":0.15155,"price_change_24h":-0.003352456798010356,"price_change_percentage_24h":-2.1601,"market_cap_change_24h":-115670324.79428482,"market_cap_change_percentage_24h":-2.11631,"circulating_supply":35372681792.97376,"total_supply":50001786837.39707,"max_supply":null,"ath":0.875563,"ath_change_percentage":-82.72636,"ath_date":"2018-01-02T16:00:00.000Z","atl":0.00047612,"atl_change_percentage":31665.21169,"atl_date":"2015-03-04T16:00:00.000Z","roi":null,"last_updated":"2026-11-07T15:47:55.000Z","price_change_percentage_1h_in_currency":0.2335,"price_change_percentage_24h_in_currency":-2.1601,"price_change_percentage_7d_in_currency":-10.355},{"id":"bitcoin-cash","symbol":"bch","name":"Bitcoin Cash","image":"https://coin-images.coingecko.com/coins/images/780/large/bitcoin-cash-circle.png?1696501932","current_price":256.7,"market_cap":5163633016,"market_cap_rank":20,"fully_diluted_valuation":5163630610,"total_volume":109912368,"high_24h":268.89,"low_24h":255.92,"price_change_24h":-11.557781813317831,"price_change_percentage_24h":-4.29457,"market_cap_change_24h":-231796753.45672035,"market_cap_change_percentage_24h":-4.29617,"circulating_supply":20113634.27165076,"total_supply":20113624.89665076,"max_supply":21000000.0,"ath":3785.82,"ath_change_percentage":-93.21954,"ath_date":"2017-12-19T16:00:00.000Z","atl":76.93,"atl_change_percentage":233.654,"atl_date":"2018-12-15T16:00:00.000Z","roi":null,"last_updated":"2026-11-07T15:47:55.000Z","price_change_percentage_1h_in_currency":0.3187,"price_change_percentage_24h_in_currency":-4.29457,"price_change_percentage_7d_in_currency":-10.4566}]"""

coins = json.loads(data)

# Stablecoins to exclude
stablecoins = {
    'tether', 'usdt', 'usd-coin', 'usdc', 'dai', 'first-digital-usd', 'usde',
    'tusd', 'usdd', 'pyusd', 'fdusd', 'paxg', 'eurc', 'eusd', 'global-dollar',
    'rlusd', 'usdg', 'stable', 'pyusd', 'sofid', 'eurcv', 'apxusd', 'usdai',
    'ausd', 'usx', 'crvusd', 'gusd', 'usdg', 'fdusd', 'usdy', 'sofid', 'eurcv',
    'apxusd', 'usdai', 'ausd', 'usx', 'crvusd', 'gusd', 'usdg', 'fdusd', 'usdy'
}

# Filter out stablecoins and illiquid tokens (< $1M volume)
filtered = []
for coin in coins:
    symbol = coin['symbol'].lower()
    if symbol in stablecoins:
        continue
    volume_usd = coin['total_volume']
    if volume_usd < 1_000_000:  # Exclude illiquid tokens
        continue
    filtered.append(coin)

# Sort by 24h change
filtered_sorted = sorted(filtered, key=lambda x: x['price_change_percentage_24h'], reverse=True)

# Get top 10 winners and losers
winners = filtered_sorted[:10]
losers = sorted(filtered_sorted[-10:], key=lambda x: x['price_change_percentage_24h'])  # Ascending (negative)

# Generate tags
def get_tags(coin):
    tags = []
    pct24 = coin['price_change_percentage_24h']
    rank = coin['market_cap_rank']
    volume = coin['total_volume']

    # Volume threshold for microcap detection
    if rank > 150 and pct24 > 30:
        tags.append('[PUMP-RISK]')

    if rank <= 20:
        tags.append('[MAJOR]')

    return tags

# Format output
output = []
output.append(f"*Token Movers — {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}*")
output.append("")
output.append("## Top Winners (24h)")

for i, coin in enumerate(winners, 1):
    price = coin['current_price']
    price_24h = coin['price_change_percentage_24h']
    price_7d = coin.get('price_change_percentage_7d', 0)
    price_1h = coin.get('price_change_percentage_1h', 0)
    vol = coin['total_volume']
    rank = coin['market_cap_rank']
    tags = get_tags(coin)

    # Format price
    if price >= 1:
        price_str = f"${price:,.2f}"
    else:
        price_str = f"${price:.6f}"

    # Format volume
    if vol >= 1_000_000_000:
        vol_str = f"${vol/1_000_000_000:.2f}B"
    elif vol >= 1_000_000:
        vol_str = f"${vol/1_000_000:.2f}M"
    elif vol >= 1_000:
        vol_str = f"${vol/1_000:.2f}K"
    else:
        vol_str = f"${vol}"

    output.append(f"{i}. {coin['name']} ({coin['symbol']}) — {price_str} {price_24h:+.2f}% / 7d {price_7d:+.2f}% / 1h {price_1h:+.2f}% • ${vol_str} / #{rank} {tags if tags else ''}")

output.append("")
output.append("## Top Losers (24h)")

for i, coin in enumerate(losers, 1):
    price = coin['current_price']
    price_24h = coin['price_change_percentage_24h']
    price_7d = coin.get('price_change_percentage_7d', 0)
    price_1h = coin.get('price_change_percentage_1h', 0)
    vol = coin['total_volume']
    rank = coin['market_cap_rank']
    tags = get_tags(coin)

    if price >= 1:
        price_str = f"${price:,.2f}"
    else:
        price_str = f"${price:.6f}"

    if vol >= 1_000_000_000:
        vol_str = f"${vol/1_000_000_000:.2f}B"
    elif vol >= 1_000_000:
        vol_str = f"${vol/1_000_000:.2f}M"
    elif vol >= 1_000:
        vol_str = f"${vol/1_000:.2f}K"
    else:
        vol_str = f"${vol}"

    output.append(f"{i}. {coin['name']} ({coin['symbol']}) — {price_str} {price_24h:+.2f}% / 7d {price_7d:+.2f}% / 1h {price_1h:+.2f}% • ${vol_str} / #{rank} {tags if tags else ''}")

print('\n'.join(output))
