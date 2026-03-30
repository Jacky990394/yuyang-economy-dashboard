import requests
import json
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("啟動【國際布蘭特原油】偵察機...")

# 1. 讀取資料庫
try:
    with open('brent_data.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
except FileNotFoundError:
    print("❌ 找不到 brent_data.json，請確認檔案是否存在。")
    exit()

# 2. 潛入 Yahoo Finance API 抓取布蘭特原油期貨 (BZ=F) 最新價格
url = "https://query1.finance.yahoo.com/v8/finance/chart/BZ=F"
# 偽裝成一般瀏覽器，避免被 Yahoo 擋在門外
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}

try:
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        
        # 從 Yahoo 的複雜資料結構中精準挑出「最新市價」
        latest_price = data['chart']['result'][0]['meta']['regularMarketPrice']
        
        print(f"\n🔍 ✅ 成功抓取！最新布蘭特原油價格：{latest_price} 美元/桶")

        # 3. 更新資料倉庫
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db["update_time"] = now_str
        db["current_price"] = str(round(latest_price, 2))
        db["history_data"][-1] = round(latest_price, 2)

        # 4. 寫回 JSON 檔案
        with open('brent_data.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
            
        print(f"📁 資料已成功寫入 brent_data.json，更新時間：{now_str}\n")
    else:
        print(f"❌ 抓取失敗: 伺服器回傳狀態碼 {response.status_code}")

except Exception as e:
    print(f"❌ 國際油價抓取失敗: {e}")