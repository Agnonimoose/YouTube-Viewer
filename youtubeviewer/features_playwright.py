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
from time import sleep
from random import choice, choices, randint, shuffle, uniform


COMMANDS = ['share', 'k', 'j', 'l', 't', 'c']
# COMMANDS = [Keys.UP, Keys.DOWN, 'share', 'k', 'j', 'l', 't', 'c']

QUALITY = {
    1: ['144p', "tiny"],
    2: ['240p', "small"],
    3: ['360p', "medium"]
}


def skip_again(page):
    try:
        skip_ad = page.locator(".ytp-ad-skip-button").first
        skip_ad.scroll_into_view_if_needed()
        sleep(1)
        skip_ad.click(timeout=100)
    except Exception as e:
        print(e)


def skip_initial_ad(page, video, duration_dict):
    video_len = duration_dict.get(video, 0)
    if video_len > 30:
        bypass_playwright.bypass_popup(page)
        try:
            skipped = False
            waited = 0
            while skipped == False:
                if page.locator(".ytp-ad-skip-button").count() == 0:
                    if waited == 30:
                        skipped = True
                    else:
                        sleep(1)
                        waited += 1
                else:
                    skip_ad = page.locator(".ytp-ad-skip-button").first
                    skip_ad.scroll_into_view_if_needed()
                    skip_ad.click(timeout=1000)
                    skipped = True

        except Exception as e:
            print(e)
            skip_again(page)


def save_bandwidth(page):
    quality_index = choices([1, 2, 3], cum_weights=(0.7, 0.9, 1.00), k=1)[0]
    try:
        random_quality = QUALITY[quality_index][0]
        settings = page.locator(".ytp-button.ytp-settings-button").first
        settings.click(timeout=1000)

        Quality = page.locator("xpath=//div[contains(text(),'Quality')]").first
        Quality.click(timeout=1000)

        sleep(1)
        quality = page.locator( f"xpath=//span[contains(string(),'{random_quality}')]").first
        quality.scroll_into_view_if_needed()
        quality.click(timeout=1000)

    except Exception as e:
        print(e)
        try:
            random_quality = QUALITY[quality_index][1]
            page.execute_script(
                f"document.getElementById('movie_player').setPlaybackQualityRange('{random_quality}')")
        except Exception as e:
            print(e)


def change_playback_speed(page, playback_speed):
    if playback_speed == 2:
        page.locator('#movie_player').press('<'*randint(1, 3))
    elif playback_speed == 3:
        page.locator('#movie_player').press('>'*randint(1, 3))


def random_command(page):
    try:
        bypass_playwright.bypass_other_popup(page)
        option = choices([1, 2], cum_weights=(0.7, 1.00), k=1)[0]
        if option == 2:
            command = choice(COMMANDS)
            if command in ['m', 't', 'c']:
                page.locator('#movie_player').press(command)
            elif command == 'k':
                if randint(1, 2) == 1:
                    page.locator('#movie_player').press(command)
                x = choice([1, 2])
                if x == 1:
                    page.locator('#movie_player').scrollIntoView()
                else:
                    page.locator('#movie_player').scroll_into_view_if_needed()

                sleep(uniform(4, 10))
                page.locator('#movie_player').scroll_into_view_if_needed()

            elif command == 'share':
                if choices([1, 2], cum_weights=(0.9, 1.00), k=1)[0] == 2:
                    page.locator("xpath=//button[@id='button' and @aria-label='Share']").first.click(timeout=1000)
                    sleep(uniform(2, 5))

            else:
                page.locator('#movie_player').press(command*randint(1, 5))
    except Exception as e:
        print(e)


def wait_for_new_page(page, previous_url=False, previous_title=False):
    for _ in range(30):
        sleep(1)
        if previous_url:
            if page.url != previous_url:
                break
        elif previous_title:
            if page.title() != previous_title:
                break


def play_next_video(page, suggested):
    shuffle(suggested)
    video_id = choice(suggested)

    for _ in range(10):
        if video_id in page.url:
            video_id = choice(suggested)
        else:
            break

    try:
        page.locator(".tp-yt-paper-button#expand").click(timeout=1000)
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

    page.evaluate(js)

    find_video = page.wait_for_selector( f'xpath=//a[@href="/watch?v={video_id}&t=0s"]', timeout=30000)

    skipped = False
    waited = 0
    while skipped == False:
        if page.locator(f'xpath=//a[@href="/watch?v={video_id}&t=0s"]').count() == 0:
            if waited == 30:
                skipped = True
            else:
                sleep(1)
                waited += 1
        else:
            skip_ad = page.locator(".ytp-ad-skip-button").first
            skip_ad.scroll_into_view_if_needed()
            skip_ad.click(timeout=1000)
            skipped = True


    find_video.scroll_into_view_if_needed()

    previous_title = page.title()
    find_video.click(timeout=1000)
    wait_for_new_page(page=page, previous_url=False,
                      previous_title=previous_title)

    return page.title()[:-10]


def play_from_channel(page, actual_channel):
    channel = page.locator('.ytd-video-owner-renderer a').all()[randint(0, 1)]
    channel.crollIntoViewIfNeeded()
    
    previous_title = page.title()
    channel.click(timeout=1000)
    wait_for_new_page(page=page, previous_url=False,
                      previous_title=previous_title)

    channel_name = page.title()[:-10]

    if randint(1, 2) == 1:
        if channel_name != actual_channel:
            raise Exception(
                f"Accidentally opened another channel : {channel_name}. Closing it...")

        x = randint(30, 50)
        sleep(x)
        output = page.locator('xpath=//yt-formatted-string[@id="title"]/a').text_content()
        log = f'Video [{output}] played for {x} seconds from channel home page : {channel_name}'
        option = 4
    else:
        sleep(randint(2, 5))
        previous_url = page.url
        page.locator("xpath=//tp-yt-paper-tab[2]").click(timeout=1000)
        wait_for_new_page(page=page, previous_url=previous_url,
                          previous_title=False)

        page.refresh()
        videos = page.wait_for_selector("xpath=//a[@id='video-title-link']", 10000)
        
        video = choice(videos)
        video.scroll_into_view_if_needed()
        sleep(randint(2, 5))
        previous_title = page.title()
        bypass_playwright.ensure_click(page, video)
        wait_for_new_page(page=page, previous_url=False,
                          previous_title=previous_title)

        output = page.title()[:-10]
        log = f'Random video [{output}] played from channel : {channel_name}'
        option = 2

        channel_name = page.locator('#upload-info a').text_content()
        if channel_name != actual_channel:
            raise Exception(
                f"Accidentally opened video {output} from another channel : {channel_name}. Closing it...")

    return output, log, option


def play_end_screen_video(page):
    try:
        page.locator('css=[title^="Pause (k)"]')
        page.locator('#movie_player').press('k')
    except Exception:
        print(e)

    total = page.evaluate("return document.getElementById('movie_player').getDuration()")
    page.evaluate(f"document.querySelector('#movie_player').seekTo({total}-{randint(2,5)})")

    end_screen = page.wait_for_selector("xpath=//*[@class='ytp-ce-covering-overlay']", timeout = 5000)

    previous_title = page.title()
    sleep(randint(2, 5))
    if end_screen:
        bypass_playwright.ensure_click(page, choice(end_screen))
    else:
        raise Exception(
            f'Unfortunately no end screen video found on this video : {previous_title[:-10]}')
    wait_for_new_page(page=page, previous_url=False,
                      previous_title=previous_title)

    return page.title()[:-10]
