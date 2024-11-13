import time
import ccxt
import statistics
import csv
import atexit
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

# 5분 동안의 가격 기록을 저장할 deque (10초마다 기록하므로 5분 동안 30개 저장)
prices = deque(maxlen=30)

# 변동성 기록 리스트
volatility_records = []

# 변동성 기준 설정 (예: 변동성이 1000 KRW 이하일 때 True 반환)
VOLATILITY_THRESHOLD = 1000

# 프로그램 시작 시각 및 시작 가격
start_time = time.time()
initial_price = None  # 시작 가격을 저장할 변수

def fetch_current_price():
    """현재 BTC/KRW의 시장가를 가져오는 함수"""
    tickers = exchange.fetch_tickers()
    current_price = tickers['BTC/KRW']['close']
    print(f"BTC 현재가는 KRW {current_price} 입니다.")
    return current_price

def get_price_change():
    """10초 전, 1분 전, 프로그램 시작 시의 가격과 비교하여 변동량과 변동률을 출력하는 함수"""
    global initial_price
    if initial_price is None:
        # 프로그램 시작 시의 초기 가격 저장
        initial_price = prices[-1]

    if len(prices) > 1:
        current_price = prices[-1]
        
        # 프로그램 시작 가격과 비교
        change_from_start = current_price - initial_price
        change_from_start_percentage = (change_from_start / initial_price) * 100 if initial_price else 0
        print(f"프로그램 시작 가격: {initial_price}, 현재가: {current_price}, 변동: {change_from_start} KRW ({change_from_start_percentage:.2f}%)")
        
        # 10초 전 가격과 비교
        price_10_seconds_ago = prices[-2]
        change_10_sec = current_price - price_10_seconds_ago
        change_10_sec_percentage = (change_10_sec / price_10_seconds_ago) * 100 if price_10_seconds_ago else 0

        # 1분 전 가격과 비교
        if len(prices) >= 7:
            price_1_minute_ago = prices[-7]
            change_1_min = current_price - price_1_minute_ago
            change_1_min_percentage = (change_1_min / price_1_minute_ago) * 100 if price_1_minute_ago else 0
            print(f"10초 전 가격: {price_10_seconds_ago}, 현재가: {current_price}, 변동: {change_10_sec} KRW ({change_10_sec_percentage:.2f}%)")
            print(f"1분 전 가격: {price_1_minute_ago}, 현재가: {current_price}, 변동: {change_1_min} KRW ({change_1_min_percentage:.2f}%)")
        else:
            print(f"10초 전 가격: {price_10_seconds_ago}, 현재가: {current_price}, 변동: {change_10_sec} KRW ({change_10_sec_percentage:.2f}%)")
        
    else:
        print("가격 기록이 충분하지 않습니다. 10초 후 다시 확인합니다.")

def check_market_volatility():
    """5분간의 변동성을 계산하고, 변동성이 기준 이하일 때 True를 반환하는 함수"""
    if len(prices) == 30:  # 5분 동안의 가격 데이터가 모두 있을 때만 실행
        volatility = statistics.stdev(prices)  # 표준 편차로 변동성 계산
        volatility_records.append(volatility)  # 변동성 기록
        print(f"최근 5분간 가격 변동성: {volatility:.2f} KRW")
        
        # 변동성 기준과 비교
        if volatility <= VOLATILITY_THRESHOLD:
            print(f"최근 5분간 변동성이 {volatility}정도로, 변동 임계치 {VOLATILITY_THRESHOLD}보다 낮습니다.")
            return True
        else:
            print(f"최근 5분간 변동성이 {volatility}정도로, 변동 임계치 {VOLATILITY_THRESHOLD}보다 높습니다.")
            return False
    else:
        print("변동성 분석중... 처음 프로그램 실행하면, 분석하는데 5분정도 걸립니다.")
        return False

def print_volatility_statistics():
    """최고, 최저, 평균 변동성을 출력하는 함수"""
    if volatility_records:
        max_volatility = max(volatility_records)
        min_volatility = min(volatility_records)
        avg_volatility = sum(volatility_records) / len(volatility_records)
        print(f"최고 변동성: {max_volatility:.2f} KRW")
        print(f"최저 변동성: {min_volatility:.2f} KRW")
        print(f"평균 변동성: {avg_volatility:.2f} KRW")

# 종료 시 CSV 파일에 기록하는 함수
def save_to_csv():
    if volatility_records:
        max_volatility = max(volatility_records)
        min_volatility = min(volatility_records)
        avg_volatility = sum(volatility_records) / len(volatility_records)
        
        # 프로그램 총 실행 경과 시간 계산
        end_time = time.time()
        elapsed_time = end_time - start_time
        days, remainder = divmod(int(elapsed_time), 86400)  # 하루는 86400초
        hours, remainder = divmod(remainder, 3600)          # 한 시간은 3600초
        minutes, seconds = divmod(remainder, 60)            # 1분은 60초
        elapsed_time_str = f"{days}일 {hours}시간 {minutes}분 {seconds}초"

        # CSV 파일에 기록
        with open("volatility_statistics.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["최고 변동성", "최저 변동성", "평균 변동성", "프로그램 실행 경과 시간"])
            writer.writerow([max_volatility, min_volatility, avg_volatility, elapsed_time_str])
        print("변동성 통계가 volatility_statistics.csv 파일에 저장되었습니다.")

# 프로그램 종료 시 save_to_csv 함수를 실행하도록 설정
atexit.register(save_to_csv)

# 10초마다 가격을 확인하고 변동성을 체크
loop_count = 0
while True:
    loop_start_time = time.time()  # 루프 시작 시간 기록
    
    current_price = fetch_current_price()
    prices.append(current_price)
    get_price_change()
    check_market_volatility()  # 5분간 변동성 확인
    print_volatility_statistics()  # 최고, 최저, 평균 변동성 출력
    
    # 경과된 시간 계산
    elapsed_seconds = loop_count * 10
    days, remainder = divmod(elapsed_seconds, 86400)  # 하루는 86400초
    hours, remainder = divmod(remainder, 3600)        # 한 시간은 3600초
    minutes, seconds = divmod(remainder, 60)          # 1분은 60초
    
    # 경과 시간 출력
    print(f'프로그램 시작한 지 {days}일 {hours}시간 {minutes}분 {seconds}초 지났습니다.\n')
    
    loop_count += 1

    # 루프 실행 시간 측정 및 10초 조정
    loop_duration = time.time() - loop_start_time
    sleep_time = max(0, 10 - loop_duration)  # 남은 시간을 계산해 양수일 때만 sleep
    time.sleep(sleep_time)
