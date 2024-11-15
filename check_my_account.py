import ccxt
import pprint
import market_analyze

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

balance = exchange.fetch_balance()
#pprint.pprint(balance) #pprint는 딕셔너리, 리스트를 그냥 이쁘게 출력하는 거임.
print(balance['free']['KRW'])

def account_KRW_amount():
    return int(balance['free']['KRW'])