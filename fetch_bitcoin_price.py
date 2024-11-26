import requests
import os
from datetime import datetime
import pytz  # pytz 설치 필요

def fetch_bitcoin_price():
    url = "https://api.upbit.com/v1/ticker"
    params = {"markets": "KRW-BTC"}
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200 and data:
        price = data[0]['trade_price']
        return price
    else:
        raise Exception("Failed to fetch Bitcoin price from Upbit API.")

def create_github_issue(title, body):
    repo = os.getenv("GITHUB_REPOSITORY")
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{repo}/issues"
    payload = {
        "title": title,
        "body": body
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        print("Issue created successfully.")
    else:
        print(f"Failed to create issue. Status code: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    try:
        # KST 시간 가져오기
        kst = pytz.timezone('Asia/Seoul')
        now = datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S")
        
        # 비트코인 가격 가져오기
        price = fetch_bitcoin_price()
        
        # 이슈 제목과 내용 생성
        title = f"Bitcoin Price Update: {now} KST"
        body = f"The current Bitcoin price is **{price:,} KRW**."
        
        # GitHub 이슈 생성
        create_github_issue(title, body)
    except Exception as e:
        print(f"Error: {e}")
