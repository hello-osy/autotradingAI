import time
import ccxt
from collections import deque

# Upbit API 설정
with open("upbit.key") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    api_secret = lines[1].strip()

exchange = ccxt.upbit(config={
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True
})

# 가격 기록을 저장할 deque, 최대 길이를 설정하여 오래된 가격은 자동 삭제
prices = deque(maxlen=7)  # 10초마다 기록하므로 1분 동안 6번 + 현재가 1개 = 총 7개 저장

def fetch_current_price():
    """현재 BTC/KRW의 시장가를 가져오는 함수"""
    tickers = exchange.fetch_tickers()
    current_price = tickers['BTC/KRW']['close']
    print(f"BTC 현재가는 KRW {current_price} 입니다.")
    return current_price

def get_price_change():
    """10초 전 및 1분 전 가격과 비교하여 변동량과 변동률을 출력하는 함수"""
    if len(prices) > 1:
        current_price = prices[-1]
        price_10_seconds_ago = prices[-2]
        change_10_sec = current_price - price_10_seconds_ago
        change_10_sec_percentage = (change_10_sec / price_10_seconds_ago) * 100 if price_10_seconds_ago else 0

        # 1분 전 가격이 있는 경우에만 변동량 계산
        if len(prices) == 7:
            price_1_minute_ago = prices[0]
            change_1_min = current_price - price_1_minute_ago
            change_1_min_percentage = (change_1_min / price_1_minute_ago) * 100 if price_1_minute_ago else 0
            print(f"10초 전 가격: {price_10_seconds_ago}, 현재가: {current_price}, 변동: {change_10_sec }KRW ({change_10_sec_percentage:.2f}%)")
            print(f"1분 전 가격: {price_1_minute_ago}, 현재가: {current_price}, 변동: {change_1_min} KRW ({change_1_min_percentage:.2f}%)")
        else:
            print(f"10초 전 가격: {price_10_seconds_ago}, 현재가: {current_price}, 변동: {change_10_sec} KRW ({change_10_sec_percentage:.2f}%)")
    else:
        print("가격 기록이 충분하지 않습니다. 10초 후 다시 확인합니다.")

# 10초마다 가격을 확인하고 변동량을 계산
while True:
    current_price = fetch_current_price()
    prices.append(current_price)
    get_price_change()
    print('')
    time.sleep(10)
