# -*- coding: Latin-1 -*-
import sys
import requests
import re
from multiprocessing.dummy import Pool
from colorama import Fore, init

init(autoreset=True)

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

fr = Fore.RED
fc = Fore.CYAN
fw = Fore.WHITE
fg = Fore.GREEN
fm = Fore.MAGENTA

print("""
[#] Create By ::
   ______      __       _______ ____   ____  _       _____ 
  / __ \ \    / /\     |__   __/ __ \ / __ \| |     / ____|
 | |  | \ \  / /  \ ______| | | |  | | |  | | |    | (___  
 | |  | |\ \/ / /\ \______| | | |  | | |  | | |     \___ \ 
 | |__| | \  / ____ \     | | | |__| | |__| | |____ ____) |
  \____/   \/_/    \_\    |_|  \____/ \____/|______|_____/ 
                          OVA-TOOLS  https://t.me/ovacloud  
                  Checker Shells [WSO - Any Shell Have Password ]
""")

requests.packages.urllib3.disable_warnings()

try:
    target = [i.strip() for i in open(sys.argv[1], mode='r').readlines()]
except IndexError:
    path = str(sys.argv[0]).split('\\')
    exit('\n  [!] Enter <' + path[len(path) - 1] + '> <sites.txt>')

def URLdomain(site):
    if site.startswith("http://"):
        site = site.replace("http://", "")
    elif site.startswith("https://"):
        site = site.replace("https://", "")
    else:
        pass
    pattern = re.compile('(.*)/')
    while re.findall(pattern, site):
        sitez = re.findall(pattern, site)
        site = sitez[0]
    return site

def protocolChange(site):
    if 'http://' in site:
        site = site.replace('http://', 'https://')
    elif 'https://' in site:
        site = site.replace('https://', 'http://')
    return site

def send_get_request(url):
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=20)
        return response.text, response.status_code
    except Exception as e:
        print("Error sending GET request to {}: {}".format(url, e))
        return "", 0

def is_injection_successful(response_text, status_code):
    success_keywords = ['Uname:', '<form method=post>Password<br><input type=password name=pass'] 
    success_status_codes = [200, 201, 204] 

    return any(keyword in response_text for keyword in success_keywords) and status_code in success_status_codes

def ovastart(url):
    try:
        response_text, status_code = send_get_request(url)

        if is_injection_successful(response_text, status_code):
            print(' -| {} --> {}[Successfully]{}'.format(url, fg, fw))
            open('Results.txt', 'a').write(url + '\n')
        else:
            print(' -| {} --> {}[Failed]{}'.format(url, fr, fw))
    except Exception as e:
        print(' -| {} --> {}[Failed]: {}{}'.format(url, fr, e, fw))

mp = Pool(150)
mp.map(ovastart, target)
mp.close()
mp.join()

print('\n [!] {}Saved in Results.txt{}'.format(fc, fw))
