from selenium import webdriver

import time
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
import streamlit as st
import pandas as pd

from utils.scrape_morningstar_selenium import getPrices, getPriceVar, getDirection


def startDriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options = chrome_options)
    return driver

def getUrls(df):
    urls = []
    for item in df["ISIN"]:
        url = "https://www.morningstar.com/search?query=" + item
        urls.append(url)
    return urls

def scraping(url):
    print(url)
    driver = startDriver()
    driver.get(url)

    try:
        driver.find_element(By.XPATH, "//section/div[2]/a[@data-v-5db0bc77]").click()
        driver.current_url
        time.sleep(7)
        price, varVal, varPerc, direction = getData(driver)
        if direction == "Down":
            varVal *= -1
            varPerc *= -1
    except NoSuchElementException or InvalidArgumentException:
        price, varVal, varPerc = "Check manually", "Check manually", "check manually"

    # df.to_excel('/Users/pdewilde/Documents/Projects/AG2R/assets/dataScraped.xlsx', index = True, header = True)

    driver.close()

    return price, varVal, varPerc
    
def getData(driver):
    price = getPrices(driver)
    varVal, varPerc = getPriceVar(driver)
    direction = getDirection(driver)
    # yieldPerYear = getYearRange(driver)
    return price, varVal, varPerc, direction

@st.cache
def setupThreads(urls):
    with ThreadPoolExecutor(max_workers = 10) as executor:
        res = list(executor.map(scraping, urls))
        
        priceNow = []
        inValuta = []
        inPercent = []
        # afterYear = []

        for i in res:
            priceNow.append(i[0])
            inValuta.append(i[1])
            inPercent.append(i[2])
            # afterYear.append(i[3])
        print(len(priceNow))

    return priceNow, inValuta, inPercent


@st.cache
def singleInvestment(ISIN: str):
    url = "https://www.morningstar.com/search?query=" + ISIN
    driver = startDriver()
    driver.get(url)

    df = pd.DataFrame()
    
    name = []
    priceNow = []
    inValuta = []
    inPercent = []
    # afterYear = []

    try:
        driver.find_element(By.XPATH, "//section/div[2]/a[@data-v-5db0bc77]").click()
        time.sleep(5)
        driver.current_url
        price, varVal, varPerc, direction = getData(driver)
        dénomination = driver.find_elements(By.XPATH, "//span[@itemprop]")[0].text
        if direction == "Down":
            varVal *= -1
            varPerc *= -1
    except NoSuchElementException:
        price, varVal, varPerc, dénomination = "Check manually", "Check manually", "check manually", "check manually"
    except InvalidArgumentException:
        price, varVal, varPerc = "Check manually", "Check manually", "check manually"
        dénomination = driver.find_elements(By.XPATH, "//span[@itemprop]")[0].text

    name.append(dénomination)
    priceNow.append(price)
    inValuta.append(varVal)
    inPercent.append(varPerc)
    # afterYear.append(yearRange)
    number = [ISIN]

    driver.close()

    df["ISIN"] = number
    df["Dénomination"] = name
    df["price"] = priceNow 
    df["difference1day (valuta)"] = inValuta
    df["difference1day (%)"] = inPercent
    # df["range (valuta; 1 year)"] = afterYear
    df.set_index("ISIN", inplace = True)

    return df
