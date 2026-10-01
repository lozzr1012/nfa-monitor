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
        # 啟動 Chromium 瀏覽器
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage'
            ]
        )
        
        # 模擬繁體中文 Windows 瀏覽器環境與台灣時區，防止被 WAF 判定為海外機器人
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            locale="zh-TW",
            timezone_id="Asia/Taipei",
            extra_http_headers={
                "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            }
        )
        page = context.new_page()
        
        # 繞過 navigator.webdriver 防火牆檢測
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        try:
            # 載入網頁並等待 DOM
            response = page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=60000)
            print(f"網頁連線狀態碼：{response.status if response else '無回應'}")
            
            # 等待 5 秒讓動態內容載入
            time.sleep(5)
            
            # 截圖並存檔
            page.screenshot(path=latest_path, full_page=False)
            page.screenshot(path=history_path, full_page=False)
            print("截圖成功！")
        except Exception as e:
            print(f"截圖失敗，原因：{e}")
        finally:
            browser.close()

if __name__ == "__main__":
    take_screenshot()
