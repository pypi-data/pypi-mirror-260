import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time
import requests
import re

from create_wallets import *
from metamask import *
from excel import *


def urljoin(*args):
    return "\\".join(map(lambda x: str(x).rstrip('\\'), args))


def regexp(exp, mes, arg=''):
    while not re.match(exp, arg):
        arg = input(mes)
    return arg


def urlcheck(surl):
    r = requests.get(surl)
    return r.status_code


def new_tabs_ch(driver):
    b = driver.current_window_handle
    for handle in driver.window_handles:
        if handle != b:
            driver.switch_to.window(handle)
            driver.close()
            driver.switch_to.window(b)


def new_wallets(b_add_wallets, rn, excel_path):
    qty_wallets = 0
    if b_add_wallets == "y":
        qty_wallets = int(regexp(r'^\d+$', 'Write number wallets: '))
        for n_wallet in range(qty_wallets):
            words = create_eth_wallet()
            input_xls(words, excel_path, rn + n_wallet)


def brw_run(s_c_run):
    try:
        print('Threds №' + s_c_run + ' will be run')
        c_run = int(s_c_run)
        root_dir = os.path.dirname(os.path.abspath(__file__))
        metamask_path = urljoin(root_dir, r'MetaMask\10.12.3_0.crx')
        excel_path = urljoin(root_dir, r'Sid_Phrases\sides')
        ch_dr_path = urljoin(root_dir, r'chromedriver_win32\chromedriver.exe')
        profiles_path = urljoin(root_dir, r'Data_profiles\profile_')
        metamask_extension_url = 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#initialize/welcome'

        book = excel_open(excel_path)
        sheet = excel_sheet(book)
        #rn = sheet.max_row
        rn = excel_sheets_rows(sheet, 0)
        #b_add_wallets = regexp(r'^[yn]$', 'Do You want add wallets?(y/n) ')
        #new_wallets(rn)
        book = excel_open(excel_path)
        sheet = excel_sheet(book)
        #rn = sheet.max_row
        options = Options()
        #options = FirefoxOptions()
        # user-agent
        #options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('start-maximized')
        options.add_argument('user-data-dir='+profiles_path + str(c_run))
        #options.add_argument("--headless")
        options.add_extension(metamask_path)
        driver = webdriver.Chrome(executable_path=ch_dr_path, options=options)
        #driver = webdriver.Firefox(options=options)
        delay = 350  # seconds
        driver.get(metamask_extension_url)
        time.sleep(1)
        new_tabs_ch(driver)
        #flurl = urlcheck('https://google.com')
        select_network = "bsc"
        spass = s_pass(sheet, c_run, 1)
        if driver.current_url == metamask_extension_url:
            meta_reg(driver, sheet, spass, c_run, delay)
            for s_network in ['polygon', 'cronos', 'optimism', 'arbitrum', 'moonriver', 'okex', 'aurora', 'avalanche', 'boba', 'bsc']: # 'heco',
                meta_network_reg(driver, delay, s_network)
        else:
            meta_unl(driver, spass, delay)
        #meta_network_select(driver, delay, select_network)
    except Exception as ex:
        print(ex)
    else:
        print('Threds №' + s_c_run + ' is runing')

        input()


