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
import os
import shutil
import sys
import json
from concurrent.futures import ThreadPoolExecutor, wait
from glob import glob
from time import sleep

import requests
from fake_headers import Headers

os.system("")


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


print(bcolors.OKGREEN + """
  ____                                    
 |  _ \ _ __ _____  ___   _               
 | |_) | '__/ _ \ \/ / | | |              
 |  __/| | | (_) >  <| |_| |              
 |_|   |_|_ \___/_/\_\\__, |_             
      / ___| |__   ___|___/| | _____ _ __ 
     | |   | '_ \ / _ \/ __| |/ / _ \ '__|
     | |___| | | |  __/ (__|   <  __/ |   
      \____|_| |_|\___|\___|_|\_\___|_|   
                                          
""" + bcolors.ENDC)

print(bcolors.OKCYAN + """
[ GitHub : https://github.com/MShawon/YouTube-Viewer ]
""" + bcolors.ENDC)


checked = {}
cancel_all = False


def backup():
    try:
        shutil.copy('GoodProxy.txt', 'ProxyBackup.txt')
        print(bcolors.WARNING +
              'GoodProxy.txt backed up in ProxyBackup.txt' + bcolors.ENDC)
    except Exception:
        pass

    print('', file=open('GoodProxy.txt', 'w'))


def clean_exe_temp(folder):
    try:
        temp_name = sys._MEIPASS.split('\\')[-1]
    except Exception:
        temp_name = None

    for f in glob(os.path.join('temp', folder, '*')):
        if temp_name not in f:
            shutil.rmtree(f, ignore_errors=True)


def load_proxy():
    proxies = []

    filename = input(bcolors.OKBLUE +
                     'Enter your proxy file name: ' + bcolors.ENDC)

    if filename[-4:] == "json":
        proxies = json.loads(open(filename, "r").read())
    else:
        if not os.path.isfile(filename) and filename[-4:] != '.txt':
            filename = f'{filename}.txt'

        try:
            with open(filename, encoding="utf-8") as fh:
                loaded = [x.strip() for x in fh if x.strip() != '']
                for lines in loaded:
                    if lines.count(':') == 3:
                        split = lines.split(':')
                        lines = f'{split[2]}:{split[-1]}@{split[0]}:{split[1]}'
                    proxies.append(lines)


        except Exception as e:
            print(bcolors.FAIL + str(e) + bcolors.ENDC)
            input('')
            sys.exit()

    return proxies

def main_checker_json(proxy_dict, position):
    if cancel_all:
        raise KeyboardInterrupt

    checked[position] = None

    try:
        header = Headers(
            headers=False
        ).generate()
        agent = header['User-Agent']

        headers = {
            'User-Agent': f'{agent}',
        }

        response = requests.get(
            'https://www.youtube.com/', headers=headers, proxies=proxy_dict, timeout=30, verify=False)
        status = response.status_code

        if status != 200:
            raise Exception(status)

        print(bcolors.OKBLUE + f"Worker {position+1} | " + bcolors.OKGREEN +
              f'| GOOD | Type : | Response : {status}' + bcolors.ENDC)

        print(f'|', file=open('GoodProxy.txt', 'a'))

    except Exception as e:
        try:
            print(e)
            e = int(e.args[0])
        except Exception as e:
            # print(e)
            e = ''
        print(bcolors.OKBLUE + f"Worker {position+1} | " + bcolors.FAIL +
              f' |  | BAD | {e}' + bcolors.ENDC)

def proxy_check_json(proxy_list, position):
    sleep(1)
    main_checker_json(proxy_list, position)


def main_json(proxy_list):
    global cancel_all

    cancel_all = False

    total_proxies = 5

    pool_number = [i for i in range(total_proxies)]

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(proxy_check_json, proxy_list, position)
                   for position in pool_number]
        done, not_done = wait(futures, timeout=0)
        try:
            while not_done:
                freshly_done, not_done = wait(not_done, timeout=5)
                done |= freshly_done
        except KeyboardInterrupt:
            print(bcolors.WARNING +
                  'Hold on!!! Allow me a moment to finish the running threads' + bcolors.ENDC)
            cancel_all = True
            for future in not_done:
                _ = future.cancel()
            _ = wait(not_done, timeout=None)
            raise KeyboardInterrupt
        except IndexError:
            print(bcolors.WARNING + 'Number of proxies are less than threads. Provide more proxies or less threads. ' + bcolors.ENDC)


def main_checker(proxy_type, proxy, position):
    if cancel_all:
        raise KeyboardInterrupt

    checked[position] = None

    try:
        proxy_dict = {
            "http": f"{proxy_type}://{proxy}",
            "https": f"{proxy_type}://{proxy}",
        }
        print("proxy_dict = ", proxy_dict)

        header = Headers(
            headers=False
        ).generate()
        agent = header['User-Agent']

        headers = {
            'User-Agent': f'{agent}',
        }

        response = requests.get(
            'https://www.youtube.com/', headers=headers, proxies=proxy_dict, timeout=30)
        status = response.status_code

        if status != 200:
            raise Exception(status)

        print(bcolors.OKBLUE + f"Worker {position+1} | " + bcolors.OKGREEN +
              f'{proxy} | GOOD | Type : {proxy_type} | Response : {status}' + bcolors.ENDC)

        print(f'{proxy}|{proxy_type}', file=open('GoodProxy.txt', 'a'))

    except Exception as e:
        try:
            e = int(e.args[0])
        except Exception:
            e = ''
        print(bcolors.OKBLUE + f"Worker {position+1} | " + bcolors.FAIL +
              f'{proxy} | {proxy_type} | BAD | {e}' + bcolors.ENDC)
        checked[position] = proxy_type


def proxy_check(position):
    sleep(2)
    proxy = proxy_list[position]

    if '|' in proxy:
        splitted = proxy.split('|')
        main_checker(splitted[-1], splitted[0], position)
    else:
        main_checker('http', proxy, position)
        if checked[position] == 'http':
            main_checker('socks4', proxy, position)
        if checked[position] == 'socks4':
            main_checker('socks5', proxy, position)


def main():
    global cancel_all

    cancel_all = False
    pool_number = [i for i in range(total_proxies)]

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(proxy_check, position)
                   for position in pool_number]
        done, not_done = wait(futures, timeout=0)
        try:
            while not_done:
                freshly_done, not_done = wait(not_done, timeout=5)
                done |= freshly_done
        except KeyboardInterrupt:
            print(bcolors.WARNING +
                  'Hold on!!! Allow me a moment to finish the running threads' + bcolors.ENDC)
            cancel_all = True
            for future in not_done:
                _ = future.cancel()
            _ = wait(not_done, timeout=None)
            raise KeyboardInterrupt
        except IndexError:
            print(bcolors.WARNING + 'Number of proxies are less than threads. Provide more proxies or less threads. ' + bcolors.ENDC)


if __name__ == '__main__':

    clean_exe_temp(folder='proxy_check')
    backup()

    try:
        threads = int(
            input(bcolors.OKBLUE+'Threads (recommended = 100): ' + bcolors.ENDC))
    except Exception:
        threads = 100

    proxy_list = load_proxy()
    # removing empty & duplicate proxies
    if isinstance(proxy_list, list):
        proxy_list = list(set(filter(None, proxy_list)))

        total_proxies = len(proxy_list)
        print(bcolors.OKCYAN +
              f'Total unique proxies : {total_proxies}' + bcolors.ENDC)

        try:
            main()
        except KeyboardInterrupt:
            sys.exit()
    else:
        total_proxies = len(proxy_list)
        print(bcolors.OKCYAN +
              f'Total unique JSON proxies : {total_proxies}' + bcolors.ENDC)


        try:
            main_json(proxy_list)
        except KeyboardInterrupt:
            sys.exit()