from pandas.core.indexes.base import Index
from scrape_morningstar_selenium import getPrices, getPriceVar, getDirection, getYield

from selenium import webdriver
import time
import pandas as pd


def getData(url: str):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options = chrome_options)
    r = driver.get(url)
    html = driver.page_source
    time.sleep(10)
    price = getPrices(driver)
    priceVar = getPriceVar(driver)
    direction = getDirection(driver)
    yieldPerYear = getYield(driver)
    driver.close()
    return price, priceVar, direction, yieldPerYear

def itterateInvestments(excelFile: str):
    df = pd.read_excel(excelFile)
    for item in Index:
        # input on website
        url = "" # new url
        price, priceVar, direction, yieldPerYear = getData(url)
        df.append(price, priceVar, direction, yieldPerYear)

def singleInvestment(ISIN: str):
    url = str + ISIN

