import time
import ccxt
import pprint
import market_analyze
import check_my_account

with open("upbit.key") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    api_secret = lines[1].strip()

exchange = ccxt.upbit(config={
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True
})

# 변수 설정
total_order_amount = 0  # 주문 총액(KRW)
account_KRW_limit = 1000001  # 현금 최소 보유량(KRW)

def buy_BTC():
    if market_analyze.buy_decision():
        if check_my_account.account_KRW_amount() >= account_KRW_limit:
            exchange.options['createMarketBuyOrderRequiresPrice'] = False
            exchange.create_market_buy_order(  # 시장가 BTC 구매 주문
                symbol="KRW-BTC",
                amount=total_order_amount  # 주문총액(KRW)
            )
            print(f'KRW {total_order_amount}만큼 시장가 BTC 구매 주문을 넣었습니다.')
        else:
            print(f"계좌에 들어있는 돈이 KRW{check_my_account.account_KRW_amount}으로, 현금 최소 보유량 {account_KRW_limit}보다 작아서 구매 주문이 불가합니다.")
    else:
        print("시장 분석 결과에 따라서, 지금은 구매 주문을 넣지 않겠습니다.")

# 10초마다 buy_BTC 호출
while True:
    buy_BTC()
    time.sleep(10)
