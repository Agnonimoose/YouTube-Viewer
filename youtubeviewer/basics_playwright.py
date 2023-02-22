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

# from .features import *
from . import features_playwright, bypass_playwright
from time import sleep
from random import choice, choices, randint, shuffle, uniform

from playwright.sync_api import sync_playwright


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

def get_driver(spoofs, proxy=None):

    playwright = sync_playwright().start()
    if proxy:
        browser = playwright.chromium.launch(proxy=proxy, headless= False)
    else:
        browser = playwright.chromium.launch(headless= False)
    context = browser.new_context(ignore_https_errors = True, bypass_csp = True, geolocation  = spoofs[0], timezone_id = spoofs[1])
    page = context.new_page()
    page.set_default_timeout(0)
    return browser, context, page

def get_driver(background, viewports, agent, auth_required, path, proxy, proxy_type, proxy_folder):
    print("get_driver(background, viewports, agent, auth_required, path, proxy, proxy_type, proxy_folder) = ", background, viewports, agent, auth_required, path, proxy, proxy_type, proxy_folder)
    try:
        options = webdriver.ChromeOptions()
        options.headless = background
        if viewports:
            options.add_argument(f"--window-size={choice(viewports)}")
        options.add_argument("--log-level=3")
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        prefs = {"intl.accept_languages": 'en_US,en',
                 "credentials_enable_service": False,
                 "profile.password_manager_enabled": False,
                 "profile.default_content_setting_values.notifications": 2,
                 "download_restrictions": 3}
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option('extensionLoadTimeout', 120000)
        options.add_argument(f"user-agent={agent}")
        options.add_argument("--mute-audio")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-features=UserAgentClientHint')
        options.add_argument("--disable-web-security")
        webdriver.DesiredCapabilities.CHROME['loggingPrefs'] = {
            'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}

        if not background:
            options.add_extension(WEBRTC)
            options.add_extension(FINGERPRINT)
            options.add_extension(ACTIVE)

            if CUSTOM_EXTENSIONS:
                for extension in CUSTOM_EXTENSIONS:
                    options.add_extension(extension)

        if auth_required:
            create_proxy_folder(proxy, proxy_folder)
            options.add_argument(f"--load-extension={proxy_folder}")
        else:
            print("get driver proxy_type = ", proxy_type)
            print("get driver proxy = ", proxy)
            print("--proxy-server={proxy_type}://{proxy} = ", f'--proxy-server={proxy_type}://{proxy}')
            options.add_argument(f'--proxy-server={proxy_type}://{proxy}')

        service = Service(executable_path=path)
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(e)
        raise e

def play_video(page):
    try:
        page.locator('css=[title^="Pause (k)"]')
    except Exception as e:
        print(e)
        try:
            page.locator('css=button.ytp-large-play-button.ytp-button').press("Enter")
        except Exception as e:
            print(e)
            try:
                page.locator('css=[title^="Play (k)"]').click(timeout=100)
            except Exception as e:
                print(e)
                try:
                    page.locator("css=button.ytp-play-button.ytp-button").click(timeout=100)
                except Exception as e:
                    print(e)

    features_playwright.skip_again(page)


def play_music(page):
    try:
        page.locator('xpath=//*[@id="play-pause-button" and @title="Pause"]')
    except Exception as e:
        print(e)
        try:
            page.locator('xpath=//*[@id="play-pause-button" and @title="Play"]').click(timeout=100)
        except Exception as e:
            print(e)
            page.locator("#play-pause-button").click(timeout=100)

    features_playwright.skip_again(page)


def type_keyword(page, keyword, retry=False):
    if retry:
        for _ in range(30):
            try:
                page.locator('css=input#search').first.click(timeout=100)
                break
            except Exception as e:
                print(e)
                sleep(3)

    input_keyword = page.locator('css=input#search').first
    input_keyword.clear()
    for letter in keyword:
        input_keyword.press(letter)
        sleep(uniform(.1, .4))

    method = randint(1, 2)
    if method == 1:
        input_keyword.send_keys(Keys.ENTER)
    else:
        icon = page.locator('xpath=//button[@id="search-icon-legacy"]').first
        bypass_playwright.ensure_click(page, icon)


def scroll_search(page, video_title):
    msg = None
    for i in range(1, 11):
        try:
            section = page.wait_for_selector( f'xpath=//ytd-item-section-renderer[{i}]')

            if page.locator(f'xpath=//ytd-item-section-renderer[{i}]').text == 'No more results':
                msg = 'failed'
                break

            if len(video_title) == 11:
                find_video = section.locator(f'xpath=//a[@id="video-title" and contains(@href, "{video_title}")]')
            else:
                find_video = section.locator(f'xpath=//*[@title="{video_title}"]')

            find_video.scroll_into_view_if_needed()
            sleep(1)
            bypass_playwright.bypass_popup(page)
            bypass_playwright.ensure_click(page, find_video)
            msg = 'success'
            break
        except Exception as e:
            print(e)
            sleep(randint(2, 5))
            page.wait_for_selector('body').press("Control+End")

    if i == 10:
        msg = 'failed'

    return msg


def search_video(page, keyword, video_title):
    try:
        type_keyword(page, keyword)
    except Exception as e:
        print(e)
        try:
            bypass_playwright.bypass_popup(page)
            type_keyword(page, keyword, retry=True)
        except Exception as e:
            print(e)
            raise Exception(
                "Slow internet speed or Stuck at recaptcha! Can't perform search keyword")

    msg = scroll_search(page, video_title)

    if msg == 'failed':
        bypass_playwright.bypass_popup(page)

        filters = page.locator('#filter-menu button')
        filters.scroll_into_view_if_needed()
        sleep(randint(1, 3))
        bypass_playwright.ensure_click(page, filters)

        sleep(randint(1, 3))
        sort = page.wait_for_selector('xpath=//div[@title="Sort by upload date"]')

        bypass_playwright.ensure_click(page, sort)

        msg = scroll_search(page, video_title)

    return msg
