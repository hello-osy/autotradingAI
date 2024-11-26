import requests
import os
from datetime import datetime

os.environ["GITHUB_REPOSITORY"] = "hello-osy/autotradingAI"

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
        price = fetch_bitcoin_price()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = f"Bitcoin Price Update: {now}"
        body = f"The current Bitcoin price is **{price:,} KRW**."
        create_github_issue(title, body)
    except Exception as e:
        print(f"Error: {e}")
