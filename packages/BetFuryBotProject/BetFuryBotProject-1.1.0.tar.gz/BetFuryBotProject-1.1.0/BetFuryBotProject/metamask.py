import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time


from excel import f_word, s_pass, s_word



def network_param(s_network_name, s_param_name):
    match s_network_name.split():
        case ["bsc"]:
            unit_to_bsc_params = {
                'name_network': 'Binance Smart Chain BEP-20',
                'url_rpc': 'https://bsc-dataseed.binance.org/',
                'chain_id': '56',
                'currency_symbol': 'BNB',
                'block_explorer_url': 'https://bscscan.com'
            }
        case ["polygon"]:
            unit_to_bsc_params = {
                'name_network': 'Polygon Mainnet',
                'url_rpc': 'https://rpc-mainnet.matic.network',
                'chain_id': '137',
                'currency_symbol': 'MATIC',
                'block_explorer_url': 'https://polygonscan.com'
            }
        case ["cronos"]:
            unit_to_bsc_params = {
                'name_network': 'Cronos Mainnet',
                'url_rpc': 'https://rpc.vvs.finance',
                'chain_id': '25',
                'currency_symbol': 'cro',
                'block_explorer_url': 'https://cronos.crypto.org/explorer/'
            }
        case ["optimism"]:
            unit_to_bsc_params = {
                'name_network': 'Optimism Mainnet',
                'url_rpc': 'https://mainnet.optimism.io',
                'chain_id': '10',
                'currency_symbol': 'ETH',
                'block_explorer_url': 'https://optimistic.etherscan.io'
            }
        case ["arbitrum"]:
            unit_to_bsc_params = {
                'name_network': 'Arbitrum Mainnet',
                'url_rpc': 'https://arb1.arbitrum.io/rpc',
                'chain_id': '42161',
                'currency_symbol': 'ETH',
                'block_explorer_url': 'https://arbiscan.io'
            }
        case ["heco"]:
            unit_to_bsc_params = {
                'name_network': 'Huobi ECO Chain Mainnet',
                'url_rpc': 'https://http-mainnet-node.huobichain.com',
                'chain_id': '128',
                'currency_symbol': 'HT',
                'block_explorer_url': 'https://hecoinfo.com/'
            }
        case ["moonriver"]:
            unit_to_bsc_params = {
                'name_network': 'Moonriver',
                'url_rpc': 'https://rpc.api.moonriver.moonbeam.network',
                'chain_id': '1285',
                'currency_symbol': 'MOVR',
                'block_explorer_url': 'https://moonriver.moonscan.io'
            }
        case ["okex"]:
            unit_to_bsc_params = {
                'name_network': 'OKEXChain',
                'url_rpc': 'https://exchainrpc.okex.org',
                'chain_id': '66',
                'currency_symbol': 'OKT',
                'block_explorer_url': 'https://www.oklink.com/okexchain/'
            }
        case ["aurora"]:
            unit_to_bsc_params = {
                'name_network': 'Aurora',
                'url_rpc': 'https://mainnet.aurora.dev/',
                'chain_id': '1313161554',
                'currency_symbol': 'ETH',
                'block_explorer_url': 'https://explorer.mainnet.aurora.dev/'
            }
        case ["avalanche"]:
            unit_to_bsc_params = {
                'name_network': 'Avalanche Network',
                'url_rpc': 'https://api.avax.network/ext/bc/C/rpc',
                'chain_id': '43114',
                'currency_symbol': 'AVAX',
                'block_explorer_url': 'https://snowtrace.io/'
            }
        case ["boba"]:
            unit_to_bsc_params = {
                'name_network': 'BOBA L2',
                'url_rpc': 'https://mainnet.boba.network',
                'chain_id': '288',
                'currency_symbol': 'ETH',
                'block_explorer_url': 'https://blockexplorer.boba.network'
            }
    r_param_value = unit_to_bsc_params.get(s_param_name, 0)
    return r_param_value


def meta_reg(driver, sheet, spass, rn, delay):
    try:
        element = WebDriverWait(driver, delay).\
            until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/button')))
    except TimeoutException:
        print('Hello page not loaded...')
    else:
        element.click()
    try:
        element = WebDriverWait(driver, delay).\
            until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/button')))
    except TimeoutException:
        print('Choice page not loaded...')
    else:
        element.click()
    try:
        element = WebDriverWait(driver, delay).\
            until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div[1]/footer/button[1]')))
    except TimeoutException:
        print('Create page not loaded...')
    else:
        element.click()
    n_word = int(f_word(sheet, rn, 1))
    if n_word != 12:
        try:
            element = WebDriverWait(driver, delay).\
                until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div[2]/form/div[1]/select')))
        except TimeoutException:
            print('Cant change sides type..')
        else:
            element.click()
            unit_n_word = {
                '12' : '//*[@id="app-content"]/div/div[2]/div/div/div[2]/form/div[1]/select/option[1]',
                '15' : '//*[@id="app-content"]/div/div[2]/div/div/div[2]/form/div[1]/select/option[2]',
                '18' : '//*[@id="app-content"]/div/div[2]/div/div/div[2]/form/div[1]/select/option[3]',
                '21' : '//*[@id="app-content"]/div/div[2]/div/div/div[2]/form/div[1]/select/option[4]',
                '24' : '//*[@id="app-content"]/div/div[2]/div/div/div[2]/form/div[1]/select/option[5]'
            }
            driver.find_element(
                By.XPATH, unit_n_word.get(str(n_word), 0))\
                .click()
    try:
        element = WebDriverWait(driver, delay).\
            until(ec.element_to_be_clickable((By.XPATH, '//*[@id="create-new-vault__terms-checkbox"]')))
    except TimeoutException:
        print('Create page not loaded...')
    else:
        for i in range(n_word):
            driver.find_element(
                By.XPATH, '//*[@id="import-srp__srp-word-' + str(i) + '"]')\
                .send_keys(s_word(sheet, rn, i+1))
        driver.find_element(
            By.XPATH, '//*[@id="password"]')\
            .send_keys(spass)
        driver.find_element(
            By.XPATH, '//*[@id="confirm-password"]')\
            .send_keys(spass)
        element.click()
        driver.find_element(
            By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div[2]/form/button')\
            .click()
    try:
        element = WebDriverWait(driver, delay).\
            until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/button')))
    except TimeoutException:
        print('Congratulation page not loaded...')
    else:
        element.click()
    try:
        element = WebDriverWait(driver, delay).\
            until(ec.element_to_be_clickable((By.XPATH, '//*[@id="popover-content"]/div/div/section/header/div/button')))
    except TimeoutException:
        print('News page not loaded...')
    else:
        element.click()


def meta_network_reg(driver, delay, s_network):
    try:
        element = WebDriverWait(driver, delay).\
            until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/span')))
    except TimeoutException:
        print('Network dropdown list not loaded... button')
    else:
        element.click()
    try:
        element = WebDriverWait(driver, delay).\
            until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/button')))
    except TimeoutException:
        print('Network add menu not loaded... button')
    else:
        element.click()
    try:
        element = WebDriverWait(driver, delay).\
            until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/label/input')))
    except TimeoutException:
        print('Network add page not loaded... button')
    else:
        element.send_keys(network_param(s_network, 'name_network'))
        driver.find_element(
            By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/label/input')\
            .send_keys(network_param(s_network, 'url_rpc'))
        driver.find_element(
            By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[3]/label/input')\
            .send_keys(network_param(s_network, 'chain_id'))
        driver.find_element(
            By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[5]/label/input')\
            .send_keys(network_param(s_network, 'block_explorer_url'))
        time.sleep(1.5)
        driver.find_element(
            By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[4]/label/input')\
            .send_keys(network_param(s_network, 'currency_symbol'))
        time.sleep(1.5)
        driver.find_element(
            By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[3]/button[2]')\
            .click()


def meta_unl(driver, spass, delay):
    try:
        element = WebDriverWait(driver, delay).\
            until(ec.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))
    except TimeoutException:
        print('Unlock page not loaded...')
    else:
        element.send_keys(spass)
        driver.find_element(
            By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/button')\
            .click()


def meta_network_select(driver, delay, select_network):
    try:
        element = WebDriverWait(driver, delay).\
            until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/span')))
    except TimeoutException:
        print('Network dropdown list not loaded... button')
    else:
        element.click()
    try:
        element = WebDriverWait(driver, delay).\
            until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[2]/li[12]/span')))
    except TimeoutException:
        print('Network dropdown list not loaded... network')
    else:
        element.click()