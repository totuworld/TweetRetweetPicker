import asyncio
import json
import os
from playwright.async_api import async_playwright, Browser, Page

async def login_and_save_session(session_file="session.json"):
    """
    Twitter에 로그인하고 세션 및 쿠키 정보를 파일에 저장합니다.
    (ID와 Password는 웹 브라우저에서 직접 입력합니다.)

    Args:
        session_file: 세션 정보를 저장할 파일 이름 (기본값: "session.json").
    """
    async with async_playwright() as p:
        browser: Browser = await p.chromium.launch(headless=False)  # headless=False로 하면 브라우저를 볼 수 있습니다.
        page: Page = await browser.new_page()

        try:
            # 이미 세션 파일이 있는지 확인
            if os.path.exists(session_file):
                with open(session_file, "r") as f:
                    session_data = json.load(f)
                    # 쿠키와 로컬 스토리지 정보를 복원합니다.
                    await page.context.storage_state(path=session_file)
                    print("Existing session loaded.")

                await page.goto("https://twitter.com/home")
                
                # 로그인 되어 있는지 확인(홈 화면 요소로 확인)
                try:
                    await page.wait_for_selector('article[data-testid="tweet"]', timeout=5000) 
                    print("Already logged in.")
                    await browser.close()
                    return
                except Exception as e:
                    print(f"Session expired or not logged in. Re-logging in. Error: {e}")
                    #세션이 만료되었거나, 로그인이 안되어 있으면, 다시 로그인합니다.
            
            # 로그인 페이지로 이동
            await page.goto("https://twitter.com/login")
            print("Please log in to Twitter in the browser window.")

            # 로그인 성공 여부 확인 (홈 화면 요소가 나타나는지 확인)
            await page.wait_for_selector('article[data-testid="tweet"]', timeout=60000) # 로그인 완료될때까지 60초 대기

            print("Logged in successfully.")

            # 세션 정보 저장
            session_data = await page.context.storage_state(path=session_file)

            print(f"Session saved to {session_file}")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await browser.close()

async def main():
    """
    로그인 및 세션 저장을 실행합니다.
    """
    await login_and_save_session()

if __name__ == "__main__":
    asyncio.run(main())
