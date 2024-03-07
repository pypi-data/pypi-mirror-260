# -*- coding: utf-8 -*-
# @time: 2024/3/6 8:58
# @author: Dyz
# @file: jcr_login.py
# @software: PyCharm
import json
import time

from playwright.async_api import async_playwright

jcr_file = '.jcr_cookies.json'


async def _login(playwright: async_playwright, auth, ws=None) -> dict:
    if ws:
        browser = await playwright.chromium.connect_over_cdp(ws)
    else:
        browser = await playwright.chromium.launch(headless=False)  # 有界面
        # browser = await playwright.chromium.launch()  # 无界面
    print('jcr 登陆中...')
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://jcr.clarivate.com/jcr/home")
    await page.wait_for_selector("input[name=\"email\"]")  # 等待元素出现
    await page.locator("input[name=\"email\"]").fill(auth[0])
    await page.locator("input[name=\"password\"]").fill(auth[1])
    await page.locator("button:has-text(\"Sign in Loading…\")").click()
    time.sleep(10)  # 再等待登录 cookies 加载完成
    cookies = await context.cookies()
    cookies_dict = dict()
    for cookie in cookies:
        cookies_dict[cookie['name']] = cookie['value']
    cookies_sre = '; '.join(item for item in [item["name"] + "=" + item["value"] for item in cookies])
    pid = cookies_dict['PSSID']
    if pid:
        print('jcr 登陆成功')

    jcr_cookies = {"cookies": cookies_sre, "pid": pid}
    with open(jcr_file, 'w', encoding='utf-8') as f:
        json.dump(jcr_cookies, f)

    # ---------------------
    await context.close()
    await browser.close()
    return jcr_cookies


async def login(auth, ws) -> dict:
    """登录jcr, 使用浏览器获取完整cookies"""

    async with async_playwright() as playwright:
        return await _login(playwright, auth, ws)


async def get_cookies(ws=None, reset=False, auth=None) -> dict:
    """加载本地cookies
    ws: 浏览器实例地址
    reset: 重新登陆
    auth = (user, pwd)
    """
    if reset:
        return await login(auth, ws)
    else:
        with open(jcr_file, encoding='utf-8') as f:
            data = f.read()
            if data:
                return json.loads(data)
        return await login(auth, ws)


if __name__ == '__main__':
    import asyncio

    asyncio.run(get_cookies(True))
