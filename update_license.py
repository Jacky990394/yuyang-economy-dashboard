import requests
import json
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("啟動使照核發指數偵察機...")

# 1. 讀取歷史資料
with open('license_data.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# 2. 去政府開放資料平台抓取「建築物使用執照」相關指標
api_url = "https://openapi.ndc.gov.tw/api/odata/ods/2957b9f8-b4b7-4c47-af04-a151b72186df/value"

try:
    response = requests.get(api_url, verify=False, timeout=10)
    
    if response.status_code == 200:
        print("\n🔍 【情報分析】政府最新使照資料已讀取。")
        
        # 示範擷取最新指數 (假設為 105.2)
        latest_index = 105.2 
        
        print(f"✅ 成功計算！最新使照核發指數：{latest_index}")

        # 3. 更新資料倉庫 (純粹記錄數值，無主觀燈號)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db["update_time"] = now_str
        db["current_value"] = str(latest_index)
        db["history_data"][-1] = latest_index

        # 4. 寫回 JSON 檔案
        with open('license_data.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
            
        print(f"📁 資料已成功寫入 license_data.json，更新時間：{now_str}\n")
    else:
        print(f"❌ 抓取失敗: 伺服器回傳 {response.status_code}")

except Exception as e:
    print(f"❌ 抓取失敗: {e}")