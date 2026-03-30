import requests
import json
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("啟動【國際黃金(台兩)】複合偵察機...")

# 1. 讀取資料庫
try:
    with open('gold_data.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
except FileNotFoundError:
    print("❌ 找不到 gold_data.json，請確認檔案是否存在。")
    exit()

# Yahoo Finance API 端點 (潛入模式)
base_url = "https://query1.finance.yahoo.com/v8/finance/chart/"
# 偽裝成一般瀏覽器
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}

try:
    # 2.A 抓取國際金價 (美元/盎司)
    gold_res = requests.get(base_url + "XAUUSD=X", headers=headers, timeout=10)
    # 2.B 抓取美元匯率 (USD/TWD)
    twd_res = requests.get(base_url + "TWD=X", headers=headers, timeout=10)
    
    if gold_res.status_code == 200 and twd_res.status_code == 200:
        gold_data = gold_res.json()
        twd_data = twd_res.json()
        
        # 解析數據
        price_usd_oz = gold_data['chart']['result'][0]['meta']['regularMarketPrice']
        exchange_rate = twd_data['chart']['result'][0]['meta']['regularMarketPrice']
        
        print(f"\n🔍 【情報分析】")
        print(f"✅ 國際金價：{price_usd_oz} 美元/盎司")
        print(f"✅ 美元匯率：{exchange_rate} TWD")
        
        # 3. 複合運算 (60/40 法則的變體，這裡是 100% 融合運算)
        # 公式：(美元/盎司 * TWD匯率) * 0.8294 [台兩/盎司] = 新台幣/台兩
        price_twd_tael = (price_usd_oz * exchange_rate) * 0.8294
        price_twd_tael = int(round(price_twd_tael, 0)) # 黃金價格通常取整數
        
        print(f"🎯 換算本土地區價格：{price_twd_tael} 新台幣/台兩")

        # 4. 更新資料倉庫
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db["update_time"] = now_str
        db["current_price"] = str(price_twd_tael)
        db["history_data"][-1] = price_twd_tael # 更新陣列最後一筆資料

        # 5. 寫回 JSON 檔案
        with open('gold_data.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
            
        print(f"📁 資料已成功寫入 gold_data.json，更新時間：{now_str}\n")
    else:
        print(f"❌ 抓取失敗: 伺服器回傳狀態碼 {gold_res.status_code} / {twd_res.status_code}")

except Exception as e:
    print(f"❌ 黃金價格 composite 抓取失敗: {e}")