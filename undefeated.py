import os
import requests
import datetime
import names
import time
import random
import threading
from bs4 import BeautifulSoup as bs
import json

from threading import Lock, Thread
from proxymanager import ProxyManager
from colorama import Fore, Style, init



init(autoreset=True)


session = requests.Session()

with open('config.json') as json_data:
    config = json.load(json_data)


class logger:
    printLock = threading.Lock()


def startup():
    print("""
    
 __    __  __    __  _______   ________  ________  _______    ______                      
/  |  /  |/  \  /  |/       \ /        |/        |/       \  /      \                     
$$ |  $$ |$$  \ $$ |$$$$$$$  |$$$$$$$$/ $$$$$$$$/ $$$$$$$  |/$$$$$$  |  ______   _______  
$$ |  $$ |$$$  \$$ |$$ |  $$ |$$ |__       $$ |   $$ |  $$ |$$ | _$$/  /      \ /       \ 
$$ |  $$ |$$$$  $$ |$$ |  $$ |$$    |      $$ |   $$ |  $$ |$$ |/    |/$$$$$$  |$$$$$$$  |
$$ |  $$ |$$ $$ $$ |$$ |  $$ |$$$$$/       $$ |   $$ |  $$ |$$ |$$$$ |$$    $$ |$$ |  $$ |
$$ \__$$ |$$ |$$$$ |$$ |__$$ |$$ |         $$ |   $$ |__$$ |$$ \__$$ |$$$$$$$$/ $$ |  $$ |
$$    $$/ $$ | $$$ |$$    $$/ $$ |         $$ |   $$    $$/ $$    $$/ $$       |$$ |  $$ |
 $$$$$$/  $$/   $$/ $$$$$$$/  $$/          $$/    $$$$$$$/   $$$$$$/   $$$$$$$/ $$/   $$/ 
                                                                                          
                                                                                          
                                                                                          
""")

    thread()

def thread():
    ask = input("Would you like to begin account generation? (y/n)")
    if ask == "y":
        for i in range(config['threadcount']):

            t = threading.Thread(target=create)
            t.start()
    else:
        quit()



def create():
    global session

    useProxies = config['useproxies']

    try:
        proxy_manager = ProxyManager('proxies.txt')
    except:
        print('no proxies detected, using proxyless mode')
        useProxies = True

    if useProxies:
        random_proxy = proxy_manager.random_proxy()
        proxee = random_proxy.get_dict() 
    else:
        proxee = None

    fName = names.get_first_name()
    lName = names.get_last_name()
    email = fName + lName + config['catchall']


    url = 'https://undefeated.com/account'

    payload = {
        'form_type': 'create_customer',
        'utf8': '✓',
        'customer[first_name]': fName,
        'customer[last_name]': lName,
        'customer[email]': email,
        'customer[password]': config['password']
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Upgrade-Insecure-Requests': '1'
    }
    
    with logger.printLock:
        print(time.strftime("[%H:%M:%S]") + Fore.CYAN + 'Grabbing cookies from home page')
    session.get('https://undefeated.com', proxies=proxee, headers=headers)


    with logger.printLock:
        print(time.strftime("[%H:%M:%S]") + Fore.YELLOW + 'Signing up')
    req = session.post(url, data=payload, headers=headers, proxies=proxee, allow_redirects=False)
    
    
    if req.text == '<html><body>You are being <a href="https://undefeated.com/challenge">redirected</a>.</body></html>':
        with logger.printLock:
            print(time.strftime("[%H:%M:%S]") + Fore.RED + 'Error creating account, possibly captcha')
    else:
        with logger.printLock:
            print(time.strftime("[%H:%M:%S]") + Fore.GREEN + "Successful account creation using %s" % (email))
            with open("undefeatedaccts.txt", "a+") as f:
                f.write(email + ':' + config['password'] + "\n")



startup()
