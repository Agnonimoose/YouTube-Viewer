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
import asyncio

from playwright.sync_api import sync_playwright

async def ensure_click(page, element):
    try:
        await element.scroll_into_view_if_needed()
        await asyncio.sleep(1)
        await element.click()
    except:
        await element.first.scroll_into_view_if_needed()
        await asyncio.sleep(1)
        await element.first.click()


async def personalization(page):
    try:
        search = await page.locator(f'xpath=//button[@aria-label="Turn {choice(["on","off"])} Search customization"]').first
        await search.scroll_into_view_if_needed()
        await asyncio.sleep(1)
        await search.click(timeout=100)

        history = await page.locator(f'xpath=//button[@aria-label="Turn {choice(["on","off"])} YouTube History"]').first
        await history.scroll_into_view_if_needed()
        await asyncio.sleep(1)
        await history.click(timeout=100)

        ad = await page.locator(f'xpath=//button[@aria-label="Turn {choice(["on","off"])} Ad personalization"]').first
        await ad.scroll_into_view_if_needed()
        await asyncio.sleep(1)
        await ad.click(timeout=100)

        confirm = await page.locator('xpath=//button[@jsname="j6LnYe"]').first
        await confirm.scroll_into_view_if_needed()
        await asyncio.sleep(1)
        await confirm.click(timeout=100)
    except Exception as e:
        print(e)


async def bypass_consent(page):
    try:
        consent = await page.get_by_role("button", name="Accept all")
        await consent.scroll_into_view_if_needed()
        await asyncio.sleep(1)
        await consent.click(timeout=100)
        if 'consent' in page.url:
            await personalization(page)

    except Exception as e:
        print(e)
        consent = await page.locator("xpath=//button[@jsname='j6LnYe']").first
        await consent.scroll_into_view_if_needed()
        await asyncio.sleep(1)
        await consent.click(timeout=100)
        if 'consent' in page.current_url:
            await personalization(page)


async def click_popup(page, element):
    await element.scroll_into_view_if_needed()
    await asyncio.sleep(1)
    await element.click(timeout=100)


async def bypass_popup(page):
    try:
        with page.expect_popup(timeout=5000) as popup_info:
            agree = await page.locator('xpath=//*[@aria-label="Accept the use of cookies and other data for the purposes described"]').first
            await click_popup(page=page, element=agree)
    except Exception as e:
        try:
            agree = await page.locator(f'xpath=//*[@aria-label="{choice(["Accept","Reject"])} the use of cookies and other data for the purposes described"]')
            await click_popup(page=page, element=agree)
        except:
            pass


async def bypass_other_popup(page):
    popups = ['Got it', 'Skip trial', 'No thanks', 'Dismiss', 'Not now']
    shuffle(popups)

    for popup in popups:
        try:
            popup = await page.locator(f"xpath=//*[@id='button' and @aria-label='{popup}']").first
            await popup.scroll_into_view_if_needed()
            await asyncio.sleep(1)
            await popup.click(timeout=100)
        except:
            pass

    try:
        popup = await page.locator('xpath=//*[@id="dismiss-button"]/yt-button-shape/button').first
        await popup.scroll_into_view_if_needed()
        await asyncio.sleep(1)
        await popup.click(timeout=100)
    except:
        pass
