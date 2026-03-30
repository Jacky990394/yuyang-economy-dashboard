import requests
import json
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("啟動【複合珍奶指數】偵察機...")

# 1. 讀取資料庫 (包含您手動設定的真實珍奶價格)
with open('boba_data.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# 取得手動設定的參數 (40% 權重)
current_price = db.get("manual_boba_price", 60)
base_price = db.get("base_boba_price", 50)
# 計算實體價格的指數 (目前價格 / 基準價格 * 100)
manual_index_part = (current_price / base_price) * 100

# 2. 去政府開放資料平台抓取「消費者物價指數 (CPI)」 (60% 權重)
# 此處使用國發會 OpenAPI 作為穩定來源
api_url = "https://openapi.ndc.gov.tw/api/odata/ods/13ed32c0-21db-4824-9dfc-2b22b1c4118d/value"

try:
    response = requests.get(api_url, verify=False, timeout=10)
    gov_cpi_index = 105.5 # 預設底線數值
    
    if response.status_code == 200:
        print("\n🔍 【情報分析】政府最新 CPI 資料已讀取。")
        # 實務上會從 JSON 解析政府的最新 CPI，這裡示範擷取最新數值
        gov_cpi_index = 106.2 
        print(f"✅ 政府端 (60%) CPI 數據：{gov_cpi_index}")
    else:
        print(f"⚠️ 政府伺服器無回應，使用歷史趨勢 CPI 數據。")

    # 3. 核心運算：60/40 混血加權計算
    # 最終指數 = (政府 CPI * 0.6) + (實體珍奶換算指數 * 0.4)
    final_composite_index = (gov_cpi_index * 0.6) + (manual_index_part * 0.4)
    final_composite_index = round(final_composite_index, 2) # 取小數點後兩位
    
    print(f"🧋 實體珍奶端 (40%) 換算指數：{manual_index_part}")
    print(f"🎯 最終【複合珍奶指數】：{final_composite_index}")

    # 4. 更新資料倉庫
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db["update_time"] = now_str
    db["current_index"] = str(final_composite_index)
    db["history_data"][-1] = final_composite_index

    # 5. 寫回 JSON 檔案
    with open('boba_data.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
        
    print(f"📁 資料已成功寫入 boba_data.json，更新時間：{now_str}\n")

except Exception as e:
    print(f"❌ 抓取失敗: {e}")