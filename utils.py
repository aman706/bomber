# utils.py

import requests
import time

MAX_RETRIES = 3
USE_TOR = False  # Set to True if using TOR
TOR_PROXIES = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}

# Global dictionary to store delivery stats
delivery_log = {}

def send_sms(api_url, phone):
    if api_url not in delivery_log:
        delivery_log[api_url] = {"success": 0, "fail": 0, "retries": 0}
    
    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            url = api_url.replace("PHONE", phone)
            proxies = TOR_PROXIES if USE_TOR else None

            response = requests.get(url, proxies=proxies, timeout=10)

            delivery_log[api_url]["retries"] += 1
            if response.status_code == 200:
                delivery_log[api_url]["success"] += 1
                print(f"[+] Sent: {url} | Status: {response.status_code}")
                return
            else:
                delivery_log[api_url]["fail"] += 1
                print(f"[!] Error {response.status_code} | Retrying...")
        except Exception as e:
            delivery_log[api_url]["fail"] += 1
            print(f"[-] Failed: {url} | {str(e)} | Retrying...")
        attempt += 1
        time.sleep(1)
