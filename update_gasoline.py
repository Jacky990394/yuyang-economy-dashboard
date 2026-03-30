import requests
import json
from datetime import datetime
import urllib3
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("啟動【汽油價格指標】偵察機...")

# 1. 讀取資料庫
try:
    with open('gasoline_data.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
except FileNotFoundError:
    print("❌ 找不到 gasoline_data.json，請確認檔案是否存在。")
    exit()

# 2. 去政府開放資料平台抓取「中油各式汽油每週零售價格」
# 這是穩定公開的 API (CSV 格式)
api_url = "https://data.cpc.com.tw/Opendata/GetPrice?type=1"

try:
    response = requests.get(api_url, verify=False, timeout=10)
    
    if response.status_code == 200:
        print("\n🔍 【情報分析】政府 Open Data 汽油資料已讀取。")
        
        # 解析 CSV (中油資料格式：變動日期, 92, 95, 98, 超柴...)
        decoded_content = response.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        
        # 通常最新的一筆會在 CSV 的最後一行，我們抓取「95無鉛汽油」
        if len(my_list) > 1:
            latest_record = my_list[-1]
            # latest_record[0] 是日期, [1] 是92, [2] 是95
            update_date = latest_record[0]
            latest_95_price = float(latest_record[2])
            
            print(f"✅ 成功抓取！中油公告最新 95 無鉛汽油價格：{latest_95_price} 元/公升 (公告日期: {update_date})")

            # 3. 更新資料倉庫 (保持中立，不設定紅綠燈)
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db["update_time"] = now_str
            db["current_price"] = str(latest_95_price)
            db["history_data"][-1] = latest_95_price # 更新陣列最後一筆資料

            # 4. 寫回 JSON 檔案
            with open('gasoline_data.json', 'w', encoding='utf-8') as f:
                json.dump(db, f, ensure_ascii=False, indent=2)
                
            print(f"📁 資料已成功寫入 gasoline_data.json，更新時間：{now_str}\n")
        else:
            print("⚠️ CSV 資料格式異常，無法擷取價格。")
    else:
        print(f"❌ 抓取失敗: 政府伺服器回傳狀態碼 {response.status_code}")

except Exception as e:
    print(f"❌ 汽油價格抓取失敗: {e}")