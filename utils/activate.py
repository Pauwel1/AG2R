from scrape_morningstar_selenium import getPrices, getPriceVar, getDirection, getYield

from selenium import webdriver
import time


def runBrowser(url: str):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options = chrome_options)
    r = driver.get(url)
    html = driver.page_source
    time.sleep(10)
    getPrices(driver)
    getPriceVar(driver)
    getDirection(driver)
    getYield(driver)
    driver.close()