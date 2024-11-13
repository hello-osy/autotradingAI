import ccxt
import pprint
import market_analze

with open("upbit.key") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    api_secret = lines[1].strip()

exchange = ccxt.upbit(config={
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True
    }
)


total_order_amount = 0 # 주문총액(KRW)

if 0:
    exchange.options['createMarketBuyOrderRequiresPrice'] = False
    exchange.create_market_buy_order( #시장가 주문
        symbol="KRW-BTC",
        amount=total_order_amount          # 주문총액(KRW)
    )