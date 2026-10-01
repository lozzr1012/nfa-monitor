import os
import time
from datetime import datetime, timezone, timedelta
from playwright.sync_api import sync_playwright

TARGET_URL = "https://www.nfa.gov.tw/cht/index.php?"

def take_screenshot():
    # 建立圖片儲存資料夾
    os.makedirs("screenshots", exist_ok=True)
    
    # 取得台灣時間 (UTC+8) 的時間戳記
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)
    timestamp = now.strftime('%Y%m%d_%H%M')
    
    latest_path = "screenshots/latest.png"         # 使用標準 PNG 格式
    history_path = f"screenshots/{timestamp}.png"  # 歷史紀錄備份

    print(f"正在前往網站截圖：{TARGET_URL}")
    with sync_playwright() as p:
        # 啟動無頭瀏覽器
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        # 設定標準解析度，並模擬真實瀏覽器 User-Agent 避免被阻擋
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # 載入網頁 (等待 domcontentloaded)
        page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=60000)
        
        # 強制等待 5 秒，確保圖片與動態元件全部渲染完成！
        time.sleep(5)
        
        # 儲存截圖
        page.screenshot(path=latest_path, full_page=False)
        page.screenshot(path=history_path, full_page=False)
        browser.close()
        
    print(f"截圖已成功儲存至：{latest_path} 與 {history_path}")

if __name__ == "__main__":
    take_screenshot()
