from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import selenium.webdriver.support.ui as UI
import pandas as pd 
import sys, os, django

sys.path.append("/path/to/dataScrapping")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dataScrapping.settings")
django.setup()

from scrappingApp.models import AllCarLink

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.autoscout24.com/")

nameCarVal, nameCar = [], []
select = UI.Select(driver.find_element("id", "make"))
for option in select.options:
    val = option.get_attribute('value')
    if val != "":
        nameCarVal.append(val)  
        nameCar.append(option.text)
driver.quit()

yearfrom = np.arange(1930, 2022)
priceto = [1000, 2000, 3000, 4000, 5000, 7500, 10000, 12500, 15000,
            17500, 20000, 22500, 25000, 30000, 40000, 45000, 50000,
            60000, 70000, 80000, 90000, 100000, 150000, 200000, 300000]

def add_links_to_db(df):
    for i in range(0, len(df)):
        AllCarLink.objects.create(link=df["car_links"][i])

def scrap_links_only():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    car_links = []

    for year in yearfrom[::-1]:
        for name in nameCar:
            for page in range(1,21):
                print(year, ", ", page, ", ", name)
                search_url=f"https://www.autoscout24.com/lst?sort=standard&fregfrom={year}&page={page}"      
                driver.get(search_url.format())
                try:
                    WebDriverWait(driver, 20).until(
                        EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="gdpr-consent-notice"]')))
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="save"]'))).click()
                except Exception:
                    pass
                elems = driver.find_elements(By.CSS_SELECTOR, "div.ListItem_wrapper__J_a_C > div.ListItem_header__uPzec > a")
                for elem in elems:
                    car_ind_link = elem.get_attribute("href")
                    car_links.append(car_ind_link)
            break
        break

    link_df = pd.DataFrame(car_links, columns=["car_links"])
    add_links_to_db(link_df)


            