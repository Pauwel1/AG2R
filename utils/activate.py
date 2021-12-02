from utils.scrape_morningstar_selenium import getPrices, getPriceVar, getDirection, getYearRange

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException
from selenium.webdriver.common.by import By
import time
import pandas as pd


def getData(driver):
    price = getPrices(driver)
    varVal, varPerc = getPriceVar(driver)
    direction = getDirection(driver)
    yieldPerYear = getYearRange(driver)
    return price, varVal, varPerc, direction, yieldPerYear

def iterateInvestments(excelFile: str):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options = chrome_options)

    t1 = time.perf_counter()
    df = pd.read_excel(excelFile)

    priceNow = []
    inValuta = []
    inPercent = []
    afterYear = []

    counter = 0

    for item in df["ISIN"]:
        counter += 1
        print(f"INDEX = {counter}", item)
        url = "https://www.morningstar.com/search?query=" + item

        driver.get(url)

        try:
            driver.find_element(By.XPATH, "//section/div[2]/a[@data-v-5db0bc77]").click()
            time.sleep(5)
            driver.current_url
            price, varVal, varPerc, direction, yearRange = getData(driver)
            if direction == "Down":
                varVal *= -1
                varPerc *= -1
            yearRange = yearRange.split()
            yearRange = float(yearRange[2]) - float(yearRange[0])
            yearRange = round(yearRange, 2)
        except NoSuchElementException or InvalidArgumentException:
            price, varVal, varPerc, yearRange = "Check manually", "Check manually", "Check manually", "check manually"

        priceNow.append(price)
        inValuta.append(varVal)
        inPercent.append(varPerc)
        afterYear.append(yearRange)

    driver.close()

    df["price"] = priceNow
    df["difference1day (valuta)"] = inValuta
    df["difference1day (%)"] = inPercent
    df["range (valuta; 1 year)"] = afterYear
    df.set_index("ISIN", inplace = False)

    # df.to_excel('/Users/pdewilde/Documents/Projects/AG2R/assets/dataScraped.xlsx', index = True, header = True)
    
    t2 = time.perf_counter()
    print("Process time = ", t2-t1)

    return df

def singleInvestment(ISIN: str):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options = chrome_options)

    url = "https://www.morningstar.com/search?query=" + ISIN

    driver.get(url)

    df = pd.DataFrame()
    
    name = []
    priceNow = []
    inValuta = []
    inPercent = []
    afterYear = []

    try:
        driver.find_element(By.XPATH, "//section/div[2]/a[@data-v-5db0bc77]").click()
        time.sleep(5)
        driver.current_url
        price, varVal, varPerc, direction, yearRange = getData(driver)
        dénomination = driver.find_elements(By.XPATH, "//span[@itemprop]")[0].text
        if direction == "Down":
            varVal *= -1
            varPerc *= -1
    except NoSuchElementException:
        price, varVal, varPerc, yearRange, dénomination = "Check manually", "Check manually", "Check manually", "check manually", "check manually"
    except InvalidArgumentException:
        price, varVal, varPerc, yearRange = "Check manually", "Check manually", "Check manually", "check manually"
        dénomination = driver.find_elements(By.XPATH, "//span[@itemprop]")[0].text

    name.append(dénomination)
    priceNow.append(price)
    inValuta.append(varVal)
    inPercent.append(varPerc)
    afterYear.append(yearRange)
    number = [ISIN]

    driver.close()

    df["ISIN"] = number
    df["Dénomination"] = name
    df["price"] = priceNow 
    df["difference1day (valuta)"] = inValuta
    df["difference1day (%)"] = inPercent
    df["range (valuta; 1 year)"] = afterYear
    df.set_index("ISIN", inplace = True)

    return df
