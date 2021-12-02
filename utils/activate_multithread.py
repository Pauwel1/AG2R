from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor

from utils.scrape_morningstar_selenium import getPrices, getPriceVar, getDirection, getYearRange


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
        time.sleep(15)
        driver.current_url
        price, varVal, varPerc, direction, yearRange = getData(driver)
        if direction == "Down":
            varVal *= -1
            varPerc *= -1
        # yearRange = yearRange.split()
        # yearRange = float(yearRange[2]) - float(yearRange[0])
        # yearRange = round(yearRange, 2)
    except NoSuchElementException or InvalidArgumentException:
        price, varVal, varPerc, yearRange = "Check manually", "Check manually", "Check manually", "check manually"

    # df.to_excel('/Users/pdewilde/Documents/Projects/AG2R/assets/dataScraped.xlsx', index = True, header = True)

    driver.close()

    return price, varVal, varPerc, yearRange
    
def getData(driver):
    price = getPrices(driver)
    varVal, varPerc = getPriceVar(driver)
    direction = getDirection(driver)
    yieldPerYear = getYearRange(driver)
    return price, varVal, varPerc, direction, yieldPerYear

def setupThreads(urls):
    with ThreadPoolExecutor(max_workers=5) as executor:
        res = list(executor.map(scraping, urls))
        
        priceNow = []
        inValuta = []
        inPercent = []
        afterYear = []

        for i in res:
            priceNow.append(i[0])
            inValuta.append(i[1])
            inPercent.append(i[2])
            afterYear.append(i[3])
        print(len(priceNow))

    return priceNow, inValuta, inPercent, afterYear