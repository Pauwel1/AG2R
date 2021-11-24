from scrape_morningstar_selenium import getPrices, getPriceVar, getDirection, getYield

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException
from selenium.webdriver.common.by import By
import time
import pandas as pd


def getData(driver):
    time.sleep(10)
    price = getPrices(driver)
    varVal, varPerc = getPriceVar(driver)
    direction = getDirection(driver)
    yieldPerYear = getYield(driver)
    driver.close()
    return price, varVal, varPerc, direction, yieldPerYear

def iterateInvestments(excelFile: str):
    df = pd.read_excel(excelFile)
    for item in df["ISIN"]:
        print(item)
        url = "https://www.morningstar.com/search?query=" + item

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        driver = webdriver.Chrome(options = chrome_options)
        driver.get(url)

        try:
            driver.find_element(By.XPATH, "//section/div[2]/a[@data-v-5db0bc77]").click()
            price, varVal, varPerc, direction, yieldPerYear = getData(driver)
        except NoSuchElementException or InvalidArgumentException:
            price, varVal, varPerc, direction, yieldPerYear = "", "", "", "Check Manually", ""
            continue
            
        df["price"] = price
        df["var (valuta)"] = varVal
        df["var (%)"] = varPerc
        df["yield per year"] = yieldPerYear
    print(df)

def singleInvestment(ISIN: str):
    url = str + ISIN

excelFile = "C:/Users/pdewilde/Documents/Projects/AG2R/assets/data.xlsx"
iterateInvestments(excelFile)