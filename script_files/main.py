import selenium.webdriver.support.ui as UI
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.autoscout24.com/")
nameCarVal, nameCar = [], []

def getMakeModel():
    select = UI.Select(driver.find_element("id", "make"))
    for option in select.options:
        val = option.get_attribute('value')
        if val != "":
            nameCarVal.append(val)
            nameCar.append(option.text)

    return nameCarVal, nameCar
