import time
from csv import DictWriter
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from datetime import datetime
import pytz
import json
from scrap_links import scrap_links_only
import sys, os, django

sys.path.append("/path/to/dataScrapping")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dataScrapping.settings")
django.setup()

from scrappingApp.models import CarDetail, CarDataIndex, DetailScrapExecutionTime, AllCarLink

execution_time = DetailScrapExecutionTime.objects.filter().values_list("startTime", "endTime")
start_execution_time, end_execution_time = execution_time[0][0], execution_time[0][1]

all_car_info = []
driver = ""

est_start_h, est_start_m, est_start_s = start_execution_time.hour, start_execution_time.minute, start_execution_time.second
est_end_h, est_end_m, est_end_s = end_execution_time.hour, end_execution_time.minute, end_execution_time.second


def current_zone_time():
    return datetime.now(pytz.timezone('Asia/karachi'))


def convert_into_seconds(hour, minute, second):
    return hour * 3600 + minute * 60 + second


def end_execution_time():
    current_time = current_zone_time()
    current_time_second = convert_into_seconds(current_time.hour, current_time.minute, current_time.second)
    endtime_in_second = convert_into_seconds(est_end_h, est_end_m, est_end_s)

    return endtime_in_second - current_time_second


def start_execution_time():
    current_time = current_zone_time()
    current_time_second = convert_into_seconds(current_time.hour, current_time.minute, current_time.second)
    est_start_total_sec = convert_into_seconds(est_start_h, est_start_m, est_start_s)
    if current_time_second >= est_start_total_sec:
        return abs(24 * 3600 * 60 * 60 - (est_start_total_sec + current_time_second))
    else:
        return abs(est_start_total_sec - current_time_second)


def add_car_data_to_db():
    df = pd.read_csv(f"./csv_files/data(cleanN).csv")
    for i in range(0, len(df)):
        CarDetail.objects.create(
            carModel=df['name'][i], carMileage=df['mileage'][i], carRegistration=df['first registration'][i],
            carPower=df['power'][i], carImage=df['image'][i],
            carGearbox=df['gearbox'][i], carEngine=df['engine size'][i], carGears=df['gears'][i],
            carFuelType=df['fuel type'][i],
            carFuelConsumption=df['fuel consumption'][i], carEmissions=df['co₂-emissions'][i],
            carColor=df['colour'][i], carManColor=df['manufacturer colour'][i], carBodyType=df['body type'][i],
            carType=df['type'][i],
            carSeats=df['seats'][i], carDoors=df['doors'][i], countryName=df['country version'][i],
            carOfferNumber=df['offer number'][i], carModelCode=df['model code'][i],
            carPreviousOwner=df['previous owner'][i],
            carrEmissionClass=df['emission class'][i], carNonSmoker=df['non-smoker vehicle'][i],
            carPrice=df['price'][i], carVAT=df['VAT'][i], carEquipment=df['equipment'][i],
            carContactName=df['contact_name'][i],
            carContactNumber=df['contact_number'][i], carContactAddress=df['contact_address'][i],
            carCompanyName=df['company_name'][i]
        )


def scrap_data(link):
    global driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    car_data = {}
    feature_data = []
    driver.get(link.format())

    try:
        try:
            WebDriverWait(driver, 20).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="gdpr-consent-notice"]')))
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="save"]'))).click()
        except Exception:
            pass
        car_image, new_data = [], []
        carname = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                                    "#__next > div > div > main > div.StageArea_container__YuNIp > div.StageArea_informationContainer__VaFP8 > div.StageArea_titleAndActionBarContainer__soRpp > div.StageTitle_container__vP9Cw > h1"))).text
        carname = " ".join(carname.lower().split("\n"))
        car_data["name"] = carname
        carprice = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                                     "#__next > div > div > main > div.StageArea_container__YuNIp > div.StageArea_informationContainer__VaFP8 > div.Price_mainPriceContainer__syzQE > div:nth-child(1) > div.PriceInfo_styledPriceRow__2fvRD > div > span"))).text
        car_data["price"], car_data["VAT"] = carprice.split("-")

        time.sleep(5)
        imgs_div = driver.find_elements(By.CSS_SELECTOR,
                                        "#__next > div > div > main > div.StageArea_container__YuNIp > div.Gallery_gallery__MDr8S > div > div > div.image-gallery-thumbnails-wrapper.bottom.thumbnails-swipe-horizontal > div > div > button > img")
        for elem in imgs_div:
            car_ind_link = elem.get_attribute("src")
            car_image.append(car_ind_link)

        car_data["image"] = car_image

        time.sleep(5)
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                          f"#__next > div > div > main > div.DetailPage_slicesContainer__wHHae > div > div > div.DetailsSection_childrenSection__NQLD7 > button"))).click()
        equipment_value = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                                            f"#__next > div > div > main > div.DetailPage_slicesContainer__wHHae > div > div > div.DetailsSection_childrenSection__NQLD7 > div > dl > dd > ul"))).text
        car_data["equipment"] = equipment_value.lower()

        contactName = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                                        f"#__next > div > div > main > div.DetailPage_slicesContainer__wHHae > div.VendorAndCtaSection_container__ivfyv > div > div.VendorData_mainContainer__AWyih > div.VendorData_bodyContainer__sJZZC > div.Contact_container__TYO5v > span.Contact_contactName__MFXhS"))).text
        contactNumber = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                                          f"#__next > div > div > main > div.DetailPage_slicesContainer__wHHae > div.VendorAndCtaSection_container__ivfyv > div > div.VendorData_mainContainer__AWyih > div.VendorData_bodyContainer__sJZZC > div.Contact_container__TYO5v > div > a"))).text
        contactAddress = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                                           f"#__next > div > div > main > div.DetailPage_slicesContainer__wHHae > div.VendorAndCtaSection_container__ivfyv > div > div.VendorData_mainContainer__AWyih > div.VendorData_bodyContainer__sJZZC > div.Department_openingHoursContainer__VP9fd > div.Department_departmentContainer__uYING > a > div"))).text
        companyName = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                                        f"#__next > div > div > main > div.DetailPage_slicesContainer__wHHae > div.VendorAndCtaSection_container__ivfyv > div > div.VendorData_mainContainer__AWyih > div.VendorData_bodyContainer__sJZZC > div.RatingsAndCompanyName_container__9_HA4 > div.RatingsAndCompanyName_dealer__HTXk_ > div:nth-child(1)"))).text

        car_data["contact_name"] = contactName.lower()
        car_data["contact_number"] = contactNumber.lower()
        car_data["contact_address"] = contactAddress.lower()
        car_data["company_name"] = companyName.lower()

        for i in range(0, 11):
            try:
                basic_data = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                                               f"#__next > div > div > main > div.DetailPage_slicesContainer__wHHae > div:nth-child({i}) > div"))).text
                feature_data.append(basic_data)
            except Exception:
                pass

        for data in feature_data:
            if data != "":
                data = data.lower().split("\n")
                data.pop(0)
                for key, val in zip(data[::2], data[1::2]):
                    car_data[key] = val

    except Exception:
        pass

    if car_data != "":
        all_car_info.append(car_data)
        keys = car_data.keys()
        with open('./csv_files/dataN.csv', 'a') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=keys)
            dictwriter_object.writerow(car_data)
            f_object.close()
    driver.quit()

    _df = pd.DataFrame(all_car_info)
    read_df = _df.copy()
    read_df = read_df[read_df["name"].notnull()]

    read_df['price'] = read_df['price'].str.replace(r'€', '', regex=True)
    read_df['price'] = read_df['price'].str.replace(r',', '', regex=True)
    read_df['price'] = read_df['price'].str.replace(r'.', '', regex=True)
    read_df['price'] = read_df['price'].str.replace(r' ', '', regex=True)

    kw_power = []
    for power in read_df["power"]:
        if power != "":
            if isinstance(power, str):
                p, _, _, _ = power.split(" ")
                kw_power.append(p)
            else:
                kw_power.append(power)
        else:
            kw_power.append("")

    read_df["power"] = kw_power

    read_df['mileage'] = read_df['mileage'].str.replace(r'km', '', regex=True)
    read_df['mileage'] = read_df['mileage'].str.replace(r',', '', regex=True)
    read_df['mileage'] = read_df['mileage'].str.replace(r' ', '', regex=True)

    fr_year = []
    for year in read_df["first registration"]:
        if isinstance(year, str):
            _, p = year.split("/")
            fr_year.append(p)
        else:
            fr_year.append(year)
    read_df["first registration"] = fr_year

    read_df['equipment'] = read_df['equipment'].str.split('\n')
    read_df.to_csv(f"csv_files/data(cleanN).csv")


def main_function():
    car_link_df = pd.read_csv("./csv_files/car_links.csv")

    while True:
        start_time = start_execution_time()
        if start_time == 1:
            car_link_index = CarDataIndex.objects.filter().values_list("queryIndex")
            for index, link in enumerate(car_link_df.car_links[:car_link_index[0][0]]):
                endtime = end_execution_time()
                if endtime >= 1:
                    scrap_data(link)
                else:
                    CarDataIndex.objects.update(queryIndex=int(index), modify_time=datetime.now(), id=1)
                    driver.quit()
                    add_car_data_to_db()
                    break
        else:
            print("link scrapping: ")
            scrap_links_only()

        time.sleep(1)
        print("delay_time: ", start_time)

main_function()
