import os
import time
from datetime import datetime, timezone, timedelta
from playwright.sync_api import sync_playwright

TARGET_URL = "https://www.nfa.gov.tw/cht/index.php?"

def take_screenshot():
    os.makedirs("screenshots", exist_ok=True)
    
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)
    timestamp = now.strftime('%Y%m%d_%H%M')
    
    latest_path = "screenshots/latest.png"
    history_path = f"screenshots/{timestamp}.png"

    print(f"正在前往網站截圖：{TARGET_URL}")
    with sync_playwright() as p:
        # 模擬標準 Chromium 瀏覽器環境
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-blink-features=AutomationControlled']
        )
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # 繞過自動化檢測
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        response = page.goto(TARGET_URL, wait_until="networkidle", timeout=90000)
        print(f"網頁回應狀態碼：{response.status if response else '無回應'}")
        
        # 強制等待 3 秒讓 CSS 與圖片完成繪製
        time.sleep(3)
        
        # 進行截圖
        page.screenshot(path=latest_path, full_page=False)
        page.screenshot(path=history_path, full_page=False)
        browser.close()
        
    print(f"截圖完成！最新圖片已儲存至 {latest_path}")

if __name__ == "__main__":
    take_screenshot()
