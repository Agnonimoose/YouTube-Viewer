"""
MIT License

Copyright (c) 2021-2023 MShawon

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
from random import choice, choices, randint, shuffle, uniform
from time import sleep

from playwright.sync_api import sync_playwright

def ensure_click(page, element):
    try:
        element.scroll_into_view_if_needed()
        sleep(1)
        element.click()
    except:
        element.first.scroll_into_view_if_needed()
        sleep(1)
        element.first.click()


def personalization(page):
    try:
        search = page.locator(f'xpath=//button[@aria-label="Turn {choice(["on","off"])} Search customization"]').first
        search.scroll_into_view_if_needed()
        sleep(1)
        search.click(timeout=100)

        history = page.locator(f'xpath=//button[@aria-label="Turn {choice(["on","off"])} YouTube History"]').first
        history.scroll_into_view_if_needed()
        sleep(1)
        history.click(timeout=100)

        ad = page.locator(f'xpath=//button[@aria-label="Turn {choice(["on","off"])} Ad personalization"]').first
        ad.scroll_into_view_if_needed()
        sleep(1)
        ad.click(timeout=100)

        confirm = page.locator('xpath=//button[@jsname="j6LnYe"]').first
        confirm.scroll_into_view_if_needed()
        sleep(1)
        confirm.click(timeout=100)
    except Exception as e:
        print(e)


def bypass_consent(page):
    try:
        consent = page.get_by_role("button", name="Accept all")
        consent.scroll_into_view_if_needed()
        sleep(1)
        consent.click(timeout=100)
        if 'consent' in page.url:
            personalization(page)

    except Exception as e:
        print(e)
        consent = page.locator("xpath=//button[@jsname='j6LnYe']").first
        consent.scroll_into_view_if_needed()
        sleep(1)
        consent.click(timeout=100)
        if 'consent' in page.current_url:
            personalization(page)


def click_popup(page, element):
    element.scroll_into_view_if_needed()
    sleep(1)
    element.click(timeout=100)


def bypass_popup(page):
    try:
        with page.expect_popup(timeout=5000) as popup_info:
            agree = page.locator('xpath=//*[@aria-label="Accept the use of cookies and other data for the purposes described"]').first
            click_popup(page=page, element=agree)
    except Exception as e:
        try:
            agree = page.locator(f'xpath=//*[@aria-label="{choice(["Accept","Reject"])} the use of cookies and other data for the purposes described"]')
            click_popup(page=page, element=agree)
        except:
            pass


def bypass_other_popup(page):
    popups = ['Got it', 'Skip trial', 'No thanks', 'Dismiss', 'Not now']
    shuffle(popups)

    for popup in popups:
        try:
            popup = page.locator(f"xpath=//*[@id='button' and @aria-label='{popup}']").first
            popup.scroll_into_view_if_needed()
            sleep(1)
            popup.click(timeout=100)
        except:
            pass

    try:
        popup = page.locator('xpath=//*[@id="dismiss-button"]/yt-button-shape/button').first
        popup.scroll_into_view_if_needed()
        sleep(1)
        popup.click(timeout=100)
    except:
        pass
