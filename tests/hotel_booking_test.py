import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.usefixtures("web_driver")

def before_each(web_driver):
    web_driver.get("https://www.expedia.co.in/")
    web_driver.maximize_window()
    time.sleep(5)

def test_site_title(web_driver):
    before_each(web_driver)
    assert web_driver.title == "Expedia Travel: Vacation Homes, Hotels, Car Rentals, Flights & More", "Title is not correct"
    print("Title is correct")
    logo = WebDriverWait(web_driver, 20).until(EC.presence_of_element_located((By.XPATH, "//img[@alt='Expedia']")))
    assert logo.is_displayed(), "Logo is not displayed"
    print("Logo is displayed")
    time.sleep(5)

def test_search_hotels(web_driver):
    before_each(web_driver)
    location = WebDriverWait(web_driver, 20).until(EC.presence_of_element_located((By. XPATH, "//button[@aria-label='Where to?']")))
    date_selector = WebDriverWait(web_driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@name='EGDSDateRange-date-selector-trigger']")))
    search_hotels = WebDriverWait(web_driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='search_button']")))
    
    # Actual test steps
    location.click()
    time.sleep(1)
    add_location = WebDriverWait(web_driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='destination_form_field']")))
    add_location.send_keys("New York", Keys.RETURN)
    time.sleep(2)
    
    # add dates
    date_selector.click()
    time.sleep(3)
    WebDriverWait(web_driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'uitk-day-button')]")))
    start_date = WebDriverWait(web_driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and descendant::div[@aria-label='Tuesday 10 June 2025']]")))
    start_date.click()
    time.sleep(2)
    end_date = WebDriverWait(web_driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and descendant::div[@aria-label='Sunday 15 June 2025']]")))
    end_date.click()
    time.sleep(2)
    apply_btn = WebDriverWait(web_driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//button[@data-stid='apply-date-selector'])[1]")))
    apply_btn.click()
    time.sleep(2)
    
    # search hotels
    time.sleep(2)
    search_hotels.click()
    WebDriverWait(web_driver, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete") # wait for page to load

def test_hotel_booking(web_driver):
    web_driver.get("https://www.expedia.co.in/Hotel-Search?destination=New%20York%20%28and%20vicinity%29%2C%20New%20York%2C%20United%20States%20of%20America&flexibility=0_DAY&d1=2025-04-10&startDate=2025-06-10&d2=2025-06-15&endDate=2025-06-15&adults=2&rooms=1&regionId=178293&isInvalidatedDate=false&upsellingNumNightsAdded=&theme=&userIntent=&semdtl=&upsellingDiscountTypeAdded=&useRewards=false&sort=RECOMMENDED")
    
    # select first hotel
    first_hotel = WebDriverWait(web_driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//a[@id='listing-content-entry'])[1]")))
    first_hotel.click()
    
    # page open in new tab
    original_window = web_driver.current_window_handle
    WebDriverWait(web_driver, 10).until(lambda driver: len(driver.window_handles) > 1)
    for window_handle in web_driver.window_handles:
        if window_handle != original_window:
            web_driver.switch_to.window(window_handle)
            break
    WebDriverWait(web_driver, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete")

    # select a room
    select_a_room = WebDriverWait(web_driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//button[@data-stid='sticky-button'])[1]")))
    select_a_room.click()
    WebDriverWait(web_driver, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    
    try:
        coupon_code = WebDriverWait(web_driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='couponCode']")))
        apply_coupon = WebDriverWait(web_driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-stid='apply-coupon']")))
        # apply coupon code
        coupon_code.send_keys("SUMMER25")
        apply_coupon.click()
        time.sleep(5)
        
        # check if coupon code is applied
        coupon_applied = WebDriverWait(web_driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='coupon-applied-message']")))
        if (coupon_applied.is_displayed()):
            print("Coupon code applied successfully")
            assert coupon_applied.is_displayed(), "Coupon code was not applied successfully"
            print("Coupon code applied successfully")
            time.sleep(5)
        else:
            print("Coupon code was not applied successfully")
            assert False, "Coupon code was not applied successfully"
    except Exception as e:
        print("Coupon code section is not displayed")
        print(e)
        assert False, "Coupon code section is not displayed"
