import os
import time

import requests
from playwright.sync_api import sync_playwright

USER_ID = os.environ.get('USER_ID')
USER_PW = os.environ.get('USER_PW')

DISCORD_WEBHOOK_ID = os.environ.get('DISCORD_WEBHOOK_ID')
DISCORD_WEBHOOK_TOKEN = os.environ.get('DISCORD_WEBHOOK_TOKEN')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Go to https://dhlottery.co.kr/user.do?method=login
    page.goto("https://dhlottery.co.kr/user.do?method=login")

    # Click [placeholder="아이디"]
    page.click("[placeholder=\"아이디\"]")

    # Fill [placeholder="아이디"]
    page.fill("[placeholder=\"아이디\"]", USER_ID)

    # Press Tab
    page.press("[placeholder=\"아이디\"]", "Tab")

    # Fill [placeholder="비밀번호"]
    page.fill("[placeholder=\"비밀번호\"]", USER_PW)

    # Press Tab
    page.press("[placeholder=\"비밀번호\"]", "Tab")

    # Press Enter
    # with page.expect_navigation(url="https://ol.dhlottery.co.kr/olotto/game/game645.do"):
    with page.expect_navigation():
        page.press("form[name=\"jform\"] >> text=로그인", "Enter")

    # time.sleep(5)

    page.goto("https://dhlottery.co.kr/userSsl.do?method=myPage")

    balance = page.query_selector("p.total_new > strong")
    table = page.query_selector(
        "table.tbl_data.tbl_data_col > tbody > tr:nth-child(1)")
    if balance and table:
        date = table.query_selector("td:nth-child(1)")
        rnd = table.query_selector("td:nth-child(2)")
        result = table.query_selector("td:nth-child(6)")
        if date and rnd and result:
            data = {
                "username":
                    f"로또6/45",
                "embeds": [{
                    "title":
                        f"{rnd.inner_text()}회차 결과",
                    "description":
                        f"구매일: {date.inner_text()}\n당첨결과: {result.inner_text()}\n잔액: {balance.inner_text()}원"
                }]
            }
            requests.post(
                f"https://discord.com/api/webhooks/{DISCORD_WEBHOOK_ID}/{DISCORD_WEBHOOK_TOKEN}",
                json=data)
    else:
        print("None")
    browser.close()
