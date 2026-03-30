import requests
import json
from datetime import datetime
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("啟動【台銀實體黃金(1台兩)】偵察機...")

try:
    with open('gold_data.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
except FileNotFoundError:
    print("❌ 找不到 gold_data.json")
    exit()

# 台銀黃金牌告價網頁
url = "https://rate.bot.com.tw/gold?Lang=zh-TW"
headers = {'User-Agent': 'Mozilla/5.0'}

try:
    response = requests.get(url, headers=headers, verify=False, timeout=10)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 尋找包含 "1台兩" 的表格欄位
        tael_cell = soup.find('td', string=lambda text: text and '1台兩' in text)
        
        if tael_cell:
            # 找到後，它的下一個兄弟節點 td 就是「本行賣出」的價格
            price_cell = tael_cell.find_next_sibling('td')
            price_str = price_cell.text.replace(',', '').strip()
            latest_price = int(price_str)
            
            print(f"\n🔍 【情報分析】")
            print(f"✅ 成功抓取！台銀「金鑽條塊(1台兩)」賣出價：{latest_price} 元")

            # 更新資料倉庫
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db["update_time"] = now_str
            db["current_price"] = str(latest_price)
            db["history_data"][-1] = latest_price

            # 寫回 JSON 檔案
            with open('gold_data.json', 'w', encoding='utf-8') as f:
                json.dump(db, f, ensure_ascii=False, indent=2)
                
            print(f"📁 資料已成功寫入 gold_data.json，更新時間：{now_str}\n")
        else:
            print("❌ 找不到 1台兩 的報價欄位，台銀網頁結構可能已改變。")
    else:
        print(f"❌ 抓取失敗: 伺服器回傳狀態碼 {response.status_code}")

except Exception as e:
    print(f"❌ 台銀黃金抓取失敗: {e}")