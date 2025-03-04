import asyncio
import json
import os
import time
import csv
from playwright.async_api import async_playwright, Browser, Page

async def get_retweeters(session_file="session.json", tweet_url="https://x.com/totuworld/status/1891774674427670800"):
    """
    특정 트윗의 리트윗 사용자 ID와 닉네임을 수집합니다.

    Args:
        session_file: 세션 정보를 저장한 파일.
        tweet_url: 리트윗 정보를 확인할 트윗 URL (retweets가 없는 URL).
    """
    retweeters = []
    unique_retweeters = set()  # 중복된 ID를 제거하기 위한 set

    async with async_playwright() as p:
        browser: Browser = await p.chromium.launch(headless=False)  # headless False 로 변경해서 확인하기 쉽게 했습니다. 필요에 따라 True로 변경하세요
        context = await browser.new_context(storage_state=session_file)  # 세션 정보를 context에 저장
        page: Page = await context.new_page()  # 세션정보를 담은 context를 활용해서 page를 생성

        try:
            # 세션 파일이 존재하는지 확인하고, 존재하면 세션을 로드합니다.
            if os.path.exists(session_file):
                print("Existing session loaded.")
            else:
                print(f"Session file '{session_file}' not found. Please run twitter_login.py first.")
                return []

            # 트윗 페이지로 이동합니다. (retweets가 없는 페이지)
            await page.goto(tweet_url)
            print(f"Moved to tweet page: {tweet_url}")

            # 페이지 진입 후 5초 대기
            print("Waiting for 5 seconds after page load...")
            await page.wait_for_timeout(5000)  # 5초 대기
            print("Wait complete.")

            # retweets가 붙은 페이지로 이동
            retweets_url = tweet_url + "/retweets"
            await page.goto(retweets_url)
            print(f"Moved to retweets page: {retweets_url}")

            # 리트윗 페이지 진입 후 5초 대기
            print("Waiting for 5 seconds after retweets page load...")
            await page.wait_for_timeout(5000)
            print("Wait complete. Start Scrolling...")

            scroll_count = 0
            max_scroll = 15 # 스크롤 횟수를 증가시켰습니다.
            scroll_delay = 3000 # 스크롤 대기시간을 증가시켰습니다.
            while scroll_count < max_scroll:
                # 스크롤 전 사용자 정보 추출
                retweet_elements = await page.query_selector_all(
                    'div[data-testid="cellInnerDiv"] button[data-testid="UserCell"]'
                )

                for element in retweet_elements:
                    try:
                        # 사용자 ID와 닉네임 추출
                        nickname_element = await element.query_selector(
                            'div[class="css-175oi2r r-1awozwy r-18u37iz r-dnmrzs"] span span'
                        )
                        nickname = await nickname_element.inner_text() if nickname_element else "N/A"

                        user_id_element = await element.query_selector(
                            'a[href^="/"][role="link"]'
                        )
                        user_id = await user_id_element.get_attribute('href') if user_id_element else "N/A"
                        user_id = user_id.replace('/', '@') if user_id != "N/A" else "N/A"

                        if user_id not in unique_retweeters:
                            retweeters.append({"user_id": user_id, "nickname": nickname})
                            unique_retweeters.add(user_id)
                        else:
                            print(f"Duplicate user_id found: {user_id}. Skipping...")

                    except Exception as e:
                        print(f"Error extracting user data: {e}")

                # 스크롤 수행
                await page.evaluate("window.scrollBy(0, window.innerHeight * 0.8)")  # 스크롤 량 조절
                print("Scroll Down")
                await page.wait_for_timeout(scroll_delay)  # 스크롤 후 대기시간 조절
                scroll_count += 1
                
                print(f"Current Retweeter Count: {len(retweeters)}") # 현재 수집된 user수를 확인하기 위한 로그 추가

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await context.close()  # context를 종료해야지만 세션이 보존됩니다.
            await browser.close()

    return retweeters


async def main():
    """
    리트윗 사용자 정보를 수집하는 기능을 실행합니다.
    """
    retweeters = await get_retweeters()

    if retweeters:
        print("Retweeters:")
        with open('retweet.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["user_id", "nickname"])
            for retweeter in retweeters:
                print(f"  User ID: {retweeter['user_id']}, Nickname: {retweeter['nickname']}")
                writer.writerow([retweeter['user_id'], retweeter['nickname']])

    else:
        print("No retweeters found.")


if __name__ == "__main__":
    asyncio.run(main())
