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
# from .bypass import *
from . import bypass_playwright
from random import choice, choices, randint, shuffle, uniform
import asyncio


COMMANDS = ['share', 'k', 'j', 'l', 't', 'c']
# COMMANDS = [Keys.UP, Keys.DOWN, 'share', 'k', 'j', 'l', 't', 'c']

QUALITY = {
    1: ['144p', "tiny"],
    2: ['240p', "small"],
    3: ['360p', "medium"]
}


async def skip_again(page):
    try:
        skip_ad = await page.locator(".ytp-ad-skip-button").first
        await skip_ad.scroll_into_view_if_needed()
        await asyncio.sleep(1)
        await skip_ad.click(timeout=100)
    except Exception as e:
        print(e)


async def skip_initial_ad(page, video, duration_dict):
    video_len = duration_dict.get(video, 0)
    if video_len > 30:
        await bypass_playwright.bypass_popup(page)
        try:
            skipped = False
            waited = 0
            while skipped == False:
                if await page.locator(".ytp-ad-skip-button").count() == 0:
                    if waited == 30:
                        skipped = True
                    else:
                        await asyncio.sleep(1)
                        waited += 1
                else:
                    skip_ad = await page.locator(".ytp-ad-skip-button").first
                    await skip_ad.scroll_into_view_if_needed()
                    await skip_ad.click(timeout=1000)
                    skipped = True

        except Exception as e:
            print(e)
            await skip_again(page)


async def save_bandwidth(page):
    quality_index = choices([1, 2, 3], cum_weights=(0.7, 0.9, 1.00), k=1)[0]
    try:
        random_quality = QUALITY[quality_index][0]
        settings = await page.locator(".ytp-button.ytp-settings-button").first
        await settings.click(timeout=1000)

        Quality = await page.locator("xpath=//div[contains(text(),'Quality')]").first
        await Quality.click(timeout=1000)

        await asyncio.sleep(1)
        quality = await page.locator( f"xpath=//span[contains(string(),'{random_quality}')]").first
        await quality.scroll_into_view_if_needed()
        await quality.click(timeout=1000)

    except Exception as e:
        print(e)
        try:
            random_quality = QUALITY[quality_index][1]
            await page.execute_script(
                f"document.getElementById('movie_player').setPlaybackQualityRange('{random_quality}')")
        except Exception as e:
            print(e)


async def change_playback_speed(page, playback_speed):
    if playback_speed == 2:
        await page.locator('#movie_player').press('<'*randint(1, 3))
    elif playback_speed == 3:
        await page.locator('#movie_player').press('>'*randint(1, 3))


async def random_command(page):
    try:
        await bypass_playwright.bypass_other_popup(page)
        option = choices([1, 2], cum_weights=(0.7, 1.00), k=1)[0]
        if option == 2:
            command = choice(COMMANDS)
            if command in ['m', 't', 'c']:
                await page.locator('#movie_player').press(command)
            elif command == 'k':
                if randint(1, 2) == 1:
                    await page.locator('#movie_player').press(command)
                x = choice([1, 2])
                if x == 1:
                    await page.locator('#movie_player').scrollIntoView()
                else:
                    await page.locator('#movie_player').scroll_into_view_if_needed()

                await asyncio.sleep(uniform(4, 10))
                await page.locator('#movie_player').scroll_into_view_if_needed()

            elif command == 'share':
                if choices([1, 2], cum_weights=(0.9, 1.00), k=1)[0] == 2:
                    await page.locator("xpath=//button[@id='button' and @aria-label='Share']").first.click(timeout=1000)
                    await asyncio.sleep(uniform(2, 5))

            else:
                await page.locator('#movie_player').press(command*randint(1, 5))
    except Exception as e:
        print(e)


async def wait_for_new_page(page, previous_url=False, previous_title=False):
    for _ in range(30):
        await asyncio.sleep(1)
        if previous_url:
            if page.url != previous_url:
                break
        elif previous_title:
            if page.title() != previous_title:
                break


async def play_next_video(page, suggested):
    shuffle(suggested)
    video_id = choice(suggested)

    for _ in range(10):
        if video_id in page.url:
            video_id = choice(suggested)
        else:
            break

    try:
        await page.locator(".tp-yt-paper-button#expand").click(timeout=1000)
        js = f'''
        var html = '<a class="yt-simple-endpoint style-scope yt-formatted-string" ' +
        'spellcheck="false" href="/watch?v={video_id}&t=0s" ' +
        'dir="auto">https://www.youtube.com/watch?v={video_id}</a><br>'

        var element = document.querySelector("#description-inline-expander > yt-formatted-string");

        element.insertAdjacentHTML( 'afterbegin', html );
        '''

    except Exception as e:
        print(e)

        js = f'''
        var html = '<a class="yt-simple-endpoint style-scope yt-formatted-string" ' +
        'spellcheck="false" href="/watch?v={video_id}&t=0s" ' +
        'dir="auto">https://www.youtube.com/watch?v={video_id}</a><br>'

        var elements = document.querySelectorAll("#description > yt-formatted-string");
        var element = elements[elements.length- 1];

        element.insertAdjacentHTML( 'afterbegin', html );
        '''

    await page.evaluate(js)

    find_video = await page.wait_for_selector( f'xpath=//a[@href="/watch?v={video_id}&t=0s"]', timeout=30000)

    skipped = False
    waited = 0
    while skipped == False:
        if await page.locator(f'xpath=//a[@href="/watch?v={video_id}&t=0s"]').count() == 0:
            if waited == 30:
                skipped = True
            else:
                await asyncio.sleep(1)
                waited += 1
        else:
            skip_ad = await page.locator(".ytp-ad-skip-button").first
            await skip_ad.scroll_into_view_if_needed()
            await skip_ad.click(timeout=1000)
            skipped = True


    await find_video.scroll_into_view_if_needed()

    previous_title = page.title()
    await find_video.click(timeout=1000)
    await wait_for_new_page(page=page, previous_url=False,
                      previous_title=previous_title)

    return page.title()[:-10]


async def play_from_channel(page, actual_channel):
    channel = await page.locator('.ytd-video-owner-renderer a').all()[randint(0, 1)]
    await channel.crollIntoViewIfNeeded()

    previous_title = page.title()
    await channel.click(timeout=1000)
    await wait_for_new_page(page=page, previous_url=False,
                      previous_title=previous_title)

    channel_name = page.title()[:-10]

    if randint(1, 2) == 1:
        if channel_name != actual_channel:
            raise Exception(
                f"Accidentally opened another channel : {channel_name}. Closing it...")

        x = randint(30, 50)
        await asyncio.sleep(x)
        output = await page.locator('xpath=//yt-formatted-string[@id="title"]/a').text_content()
        log = f'Video [{output}] played for {x} seconds from channel home page : {channel_name}'
        option = 4
    else:
        await asyncio.sleep(randint(2, 5))
        previous_url = page.url
        await page.locator("xpath=//tp-yt-paper-tab[2]").click(timeout=1000)
        await wait_for_new_page(page=page, previous_url=previous_url,
                          previous_title=False)

        page.reload()
        videos = page.wait_for_selector("xpath=//a[@id='video-title-link']", 10000)

        video = choice(videos)
        video.scroll_into_view_if_needed()
        await asyncio.sleep(randint(2, 5))
        previous_title = page.title()
        await bypass_playwright.ensure_click(page, video)
        await wait_for_new_page(page=page, previous_url=False,
                          previous_title=previous_title)

        output = page.title()[:-10]
        log = f'Random video [{output}] played from channel : {channel_name}'
        option = 2

        channel_name = await page.locator('#upload-info a').text_content()
        if channel_name != actual_channel:
            raise Exception(
                f"Accidentally opened video {output} from another channel : {channel_name}. Closing it...")

    return output, log, option


async def play_end_screen_video(page):
    try:
        page.locator('css=[title^="Pause (k)"]')
        page.locator('#movie_player').press('k')
    except Exception:
        print(e)

    total = page.evaluate("return document.getElementById('movie_player').getDuration()")
    page.evaluate(f"document.querySelector('#movie_player').seekTo({total}-{randint(2,5)})")

    end_screen = page.wait_for_selector("xpath=//*[@class='ytp-ce-covering-overlay']", timeout = 5000)

    previous_title = page.title()
    await asyncio.sleep(randint(2, 5))
    if end_screen:
        bypass_playwright.ensure_click(page, choice(end_screen))
    else:
        raise Exception(
            f'Unfortunately no end screen video found on this video : {previous_title[:-10]}')
    wait_for_new_page(page=page, previous_url=False,
                      previous_title=previous_title)

    return page.title()[:-10]
