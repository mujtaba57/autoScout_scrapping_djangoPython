from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import selenium.webdriver.support.ui as UI
from datetime import datetime
import pytz
import pandas as pd 
import sys, os, django
import numpy as np
sys.path.append("/path/to/dataScrapping")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dataScrapping.settings")
django.setup()

from scrappingApp.models import CarLink, LinksIndex, LinkScrapTime

execution_time = LinkScrapTime.objects.filter().values_list("startTime", "endTime")
start_execution_time, end_execution_time = execution_time[0][0], execution_time[0][1]

est_start_h, est_start_m, est_start_s = start_execution_time.hour, start_execution_time.minute, start_execution_time.second
est_end_h, est_end_m, est_end_s = end_execution_time.hour, end_execution_time.minute, end_execution_time.second

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.autoscout24.com/")
#
nameCarVal, nameCar = [], []
select = UI.Select(driver.find_element("id", "make"))
for option in select.options:
    val = option.get_attribute('value')
    if val != "":
        nameCarVal.append(val)
        nameCar.append(option.text)


priceCarVal, priceCar = [], []
select = UI.Select(driver.find_element("id", "price"))
for option in select.options:
    val = option.get_attribute('value')
    if val != "":
        priceCarVal.append(val)
        priceCar.append(option.text)


yearCarVal, yearCar = [], []
select = UI.Select(driver.find_element("id", "firstRegistration"))
for option in select.options:
    val = option.get_attribute('value')
    if val != "":
        yearCarVal.append(val)
        yearCar.append(option.text)

driver.quit()
def current_zone_time():
    return datetime.now(pytz.timezone('Asia/karachi'))


def convert_into_seconds(hour, minute, second):
    return hour * 3600 + minute * 60 + second


def end_execution_time_func():
    current_time = current_zone_time()
    current_time_second = convert_into_seconds(current_time.hour, current_time.minute, current_time.second)
    endtime_in_second = convert_into_seconds(est_end_h, est_end_m, est_end_s)

    return endtime_in_second - current_time_second


def start_execution_time_func():
    current_time = current_zone_time()
    current_time_second = convert_into_seconds(current_time.hour, current_time.minute, current_time.second)
    est_start_total_sec = convert_into_seconds(est_start_h, est_start_m, est_start_s)
    if current_time_second >= est_start_total_sec:
        return abs(24 * 3600 * 60 * 60 - (est_start_total_sec + current_time_second))
    else:
        return abs(est_start_total_sec - current_time_second)


def add_links_to_db(df):
    for i in range(0, len(df)):
        try:
            CarLink.objects.create(carlinks=df["car_links"][i])
        except Exception:
            pass

def scrap_links_only(year, price, name):
    car_links = []
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    search_url = f"https://www.autoscout24.com/lst/{name}?sort=standard&desc=0&ustate=N,U&atype=C&priceto={price}&fregfrom={year}"
    driver.get(search_url.format())
    try:
        iframe = driver.find_element(By.XPATH, '//*[@id="as24-cmp-popup"]')
        driver.execute_script("arguments[0].remove();", iframe)
    except Exception:
        pass

    pager_elems = driver.find_elements(By.CSS_SELECTOR, "div.ListPage_pagination__v_4ci > nav > ul > li")
    page_num = 0
    for elem in pager_elems[1:len(pager_elems) - 2]:
        page_num = elem.text

    if int(page_num):
        for page in range(1, int(page_num)):
            search_url = f"https://www.autoscout24.com/lst/{name}?sort=standard&desc=0&ustate=N,U&atype=C&priceto={price}&fregfrom={year}&page={page}"
            driver.get(search_url.format())
            try:
                iframe = driver.find_element(By.XPATH, '//*[@id="as24-cmp-popup"]')
                driver.execute_script("arguments[0].remove();", iframe)
            except Exception:
                pass
            elems = driver.find_elements(By.CSS_SELECTOR,
                                         "div.ListItem_wrapper__J_a_C > div.ListItem_header__uPzec > a")
            for elem in elems:
                car_ind_link = elem.get_attribute("href")
                car_links.append(car_ind_link)

    return car_links


def main_function():
    while True:
        start_time = start_execution_time_func()
        if start_time == 1:
            link_list = []
            links_list = LinksIndex.objects.filter().values_list("yearQueryIndex", "priceQueryIndex", "carNameQueryIndex")
            years_index, price_index, car_index = links_list[0][0], links_list[0][1], links_list[0][2]
            for index_year, year in enumerate(yearCarVal[years_index:]):
                endtime = end_execution_time_func()
                if endtime >= 1:
                    for price_index, price in enumerate(priceCarVal[price_index:]):
                        endtime = end_execution_time_func()
                        if endtime >= 1:
                            for car_index, name in enumerate(nameCar[car_index:]):
                                endtime = end_execution_time_func()
                                if endtime >= 1:
                                    link_data = scrap_links_only(year, price, name)
                                    link_list.extend(link_data)
                                else:
                                    link_df = pd.DataFrame(link_list, columns=["car_links"])
                                    add_links_to_db(link_df)
                                    LinksIndex.objects.update(yearQueryIndex=years_index,
                                                              priceQueryIndex=price_index,
                                                              carNameQueryIndex=car_index,
                                                              modify_time=datetime.now(),
                                                                id=1)
                                    break
                        else:
                            break
                else:
                    break

        time.sleep(1)
        print("delay_time: ", start_time)


main_function()
            