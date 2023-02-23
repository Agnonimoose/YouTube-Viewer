"""
MIT License

Copyright (c) 2021-2022 MShawon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os
from glob import glob

from . import features_playwright, bypass_playwright
from random import choice, choices, randint, shuffle, uniform

import asyncio
from playwright.async_api import async_playwright

WEBRTC = os.path.join('YouTube-Viewer/extension', 'webrtc_control.zip')
ACTIVE = os.path.join('YouTube-Viewer/extension', 'always_active.zip')
FINGERPRINT = os.path.join('YouTube-Viewer/extension', 'fingerprint_defender.zip')
CUSTOM_EXTENSIONS = glob(os.path.join('YouTube-Viewer/extension', 'custom_extension', '*.zip')) + \
                    glob(os.path.join('YouTube-Viewer/extension', 'custom_extension', '*.crx'))


def create_proxy_folder(proxy, folder_name):
    proxy = proxy.replace('@', ':')
    proxy = proxy.split(':')
    manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
 """

    background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };
chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}
chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (proxy[2], proxy[-1], proxy[0], proxy[1])

    os.makedirs(folder_name, exist_ok=True)
    with open(os.path.join(folder_name, "manifest.json"), 'w') as fh:
        fh.write(manifest_json)

    with open(os.path.join(folder_name, "background.js"), 'w') as fh:
        fh.write(background_js)

async def get_driver(spoofs, proxy=None):

    playwright = await async_playwright().start()
    if proxy:
        browser = await playwright.chromium.launch(proxy=proxy, headless= False)
    else:
        browser = await playwright.chromium.launch(headless= False)
    context = await browser.new_context(ignore_https_errors = True, bypass_csp = True, geolocation  = spoofs[0], timezone_id = spoofs[1])
    page = await context.new_page()
    page.set_default_timeout(0)
    return browser, context, page


async def play_video(page):
    try:
        await page.locator('css=[title^="Pause (k)"]')
    except Exception as e:
        print(e)
        try:
            await page.locator('css=button.ytp-large-play-button.ytp-button').press("Enter")
        except Exception as e:
            print(e)
            try:
                await page.locator('css=[title^="Play (k)"]').click(timeout=100)
            except Exception as e:
                print(e)
                try:
                    await page.locator("css=button.ytp-play-button.ytp-button").click(timeout=100)
                except Exception as e:
                    print(e)

    await features_playwright.skip_again(page)


async def play_music(page):
    try:
        await page.locator('xpath=//*[@id="play-pause-button" and @title="Pause"]')
    except Exception as e:
        print(e)
        try:
            await page.locator('xpath=//*[@id="play-pause-button" and @title="Play"]').click(timeout=100)
        except Exception as e:
            print(e)
            await page.locator("#play-pause-button").click(timeout=100)

    await features_playwright.skip_again(page)


async def type_keyword(page, keyword, retry=False):
    if retry:
        for _ in range(30):
            try:
                await page.locator('css=input#search').first.click(timeout=100)
                break
            except Exception as e:
                print(e)
                await asyncio.sleep(3)

    input_keyword = await page.locator('css=input#search').first
    await input_keyword.clear()
    for letter in keyword:
        await input_keyword.press(letter)
        await asyncio.sleep(uniform(.1, .4))

    method = randint(1, 2)
    if method == 1:
        await input_keyword.press("Enter")
    else:
        icon = await page.locator('xpath=//button[@id="search-icon-legacy"]').first
        await bypass_playwright.ensure_click(page, icon)


async def scroll_search(page, video_title):
    msg = None
    for i in range(1, 11):
        try:
            section = await page.wait_for_selector( f'xpath=//ytd-item-section-renderer[{i}]')

            if await page.locator(f'xpath=//ytd-item-section-renderer[{i}]').text == 'No more results':
                msg = 'failed'
                break

            if len(video_title) == 11:
                find_video = await section.locator(f'xpath=//a[@id="video-title" and contains(@href, "{video_title}")]')
            else:
                find_video = await section.locator(f'xpath=//*[@title="{video_title}"]')

            await find_video.scroll_into_view_if_needed()
            await asyncio.sleep(1)
            await bypass_playwright.bypass_popup(page)
            await bypass_playwright.ensure_click(page, find_video)
            msg = 'success'
            break
        except Exception as e:
            print(e)
            await asyncio.sleep(randint(2, 5))
            await page.wait_for_selector('body').press("Control+End")

    if i == 10:
        msg = 'failed'

    return msg


async def search_video(page, keyword, video_title):
    try:
        await type_keyword(page, keyword)
    except Exception as e:
        print(e)
        try:
            await bypass_playwright.bypass_popup(page)
            await type_keyword(page, keyword, retry=True)
        except Exception as e:
            print(e)
            raise Exception(
                "Slow internet speed or Stuck at recaptcha! Can't perform search keyword")

    msg = await scroll_search(page, video_title)

    if msg == 'failed':
        await bypass_playwright.bypass_popup(page)

        filters = await page.locator('#filter-menu button')
        await filters.scroll_into_view_if_needed()
        await asyncio.sleep(randint(1, 3))
        await bypass_playwright.ensure_click(page, filters)

        await asyncio.sleep(randint(1, 3))
        sort = await page.wait_for_selector('xpath=//div[@title="Sort by upload date"]')

        await bypass_playwright.ensure_click(page, sort)

        msg = await scroll_search(page, video_title)

    return msg
