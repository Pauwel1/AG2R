from selenium.webdriver.common.by import By
import re


def getPrices(driver):
    prices = driver.find_elements(By.ID, "message-box-price")
    try:
        price = prices[0].text.strip("€")
    except IndexError:
        price = "Check manually"
    return price

def getPriceVar(driver):
    priceVar = driver.find_elements(By.ID, "message-box-percentage")
    try:
        priceVar = priceVar[0].text
        priceVar = re.findall("\d*\.?\d+", priceVar)
        priceVar = list(map(float, priceVar))
        varVal = priceVar[0]
        varPerc = priceVar[1]
    except IndexError:
        varVal = "Check manually"
        varPerc = "Check manually"
    return varVal, varPerc

def getDirection(driver):
    direction = driver.find_elements(By.XPATH, '//span[@data-mds-icon-name="ip-performance-arrow-down"]')
    if len(direction) > 0:
        priceTrend = "Down"
    else:
        priceTrend = "Up"
    return priceTrend

def getYearRange(driver):
    try:
        yearRange = driver.find_elements(By.CLASS_NAME, "sal-dp-value")[5].text
    except IndexError:
        yearRange = driver.find_elements(By.CLASS_NAME, "sal-dp-value")[6].text
    return yearRange
