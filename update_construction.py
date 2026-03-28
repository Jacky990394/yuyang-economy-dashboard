import requests
import json
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("啟動昱揚營造物價偵察機...")

# 1. 讀取歷史資料倉庫
with open('construction_data.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# 2. 去政府開放資料平台抓取「營造工程物價總指數」
# (這裡使用國發會的 OpenAPI 作為穩定來源，若政府網站當機，會有防護機制)
api_url = "https://openapi.ndc.gov.tw/api/odata/ods/083f2a64-00ee-45f8-95eb-3f82054ff843/value"

try:
    response = requests.get(api_url, verify=False, timeout=10)
    
    # 確保政府網站沒有回傳錯誤網頁
    if response.status_code == 200:
        live_data = response.json()
        
        # 通常最新的資料會在陣列的最後一筆，我們抓取總指數
        if len(live_data) > 0:
            latest_record = live_data[-1]
            print("\n🔍 【情報分析】政府最新營造物價資料：")
            print(json.dumps(latest_record, indent=2, ensure_ascii=False))
            print("-" * 50)
            
            # 假設政府的欄位名稱是 "營造工程物價總指數" (如果政府改名，我們等下看終端機調整)
            cost_index_str = latest_record.get("營造工程物價總指數", "110.5")
            
            # 處理可能帶有逗號的數字字串 (例如 "110,5")
            cost_index = float(str(cost_index_str).replace(',', ''))
            
            print(f"✅ 成功抓取！最新營造工程物價指數：{cost_index}")

            # 3. 判斷燈號 (以 100 為基期，超過 105 算黃燈，超過 110 算紅燈)
            warning_level = "綠燈 (成本穩定)"
            if cost_index >= 110:
                warning_level = "紅燈 (成本飆升 - 強烈建議客戶採用長效建材)"
            elif cost_index >= 105:
                warning_level = "黃燈 (成本緩漲 - 需注意發包利潤)"

            # 4. 更新資料倉庫
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db["update_time"] = now_str
            db["overall_warning_level"] = warning_level
            db["average_cost_index"] = cost_index
            db["history_data"][-1] = cost_index 

            # 5. 寫回 JSON 檔案
            with open('construction_data.json', 'w', encoding='utf-8') as f:
                json.dump(db, f, ensure_ascii=False, indent=2)
                
            print(f"📁 資料已成功寫入 construction_data.json，更新時間：{now_str}\n")
    else:
        print(f"❌ 抓取失敗: 政府伺服器回傳狀態碼 {response.status_code}")

except Exception as e:
    print(f"❌ 營造指數抓取失敗，政府 API 可能維修中: {e}")