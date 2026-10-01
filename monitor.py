import os
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
    
    latest_path = "screenshots/latest.png"         # 永遠覆蓋最新的一張
    history_path = f"screenshots/{timestamp}.png"  # 歷史紀錄備份

    print(f"正在前往網站截圖：{TARGET_URL}")
    with sync_playwright() as p:
        # 啟動無頭瀏覽器
        browser = p.chromium.launch(headless=True)
        # 設定標準 Full HD 解析度
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        
        # 載入網頁並等待網路停止載入
        page.goto(TARGET_URL, wait_until="networkidle", timeout=60000)
        
        # 儲存截圖 (改用 jpeg 格式或優化 quality，讓 GitHub 100% 能預覽)
        page.screenshot(path=latest_path, full_page=False, type="jpeg", quality=80)
        page.screenshot(path=history_path, full_page=False, type="jpeg", quality=80)
        browser.close()
        
    print(f"截圖已成功儲存至：{latest_path} 與 {history_path}")

if __name__ == "__main__":
    take_screenshot()
