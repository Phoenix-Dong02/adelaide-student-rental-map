from playwright.sync_api import sync_playwright

APP_URL = "https://rentmapau.com"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(APP_URL, timeout=60000)
        page.wait_for_timeout(3000)

        # 如果撞上了睡眠页，点一下唤醒按钮
        wake_button = page.get_by_text("Yes, get this app back up!")
        if wake_button.count() > 0:
            wake_button.click()
            page.wait_for_timeout(15000)  # 等它真正重新拉起

        browser.close()

if __name__ == "__main__":
    main()