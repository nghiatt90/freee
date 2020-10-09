from selenium import webdriver
from selenium.common import exceptions as sce
from selenium.webdriver.common import action_chains as ac
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get('https://accounts.secure.freee.co.jp/login/hr')

email_box = driver.find_element_by_id('user_email')
password_box = driver.find_element_by_name('password')

email_box.send_keys('your.email@tokyotechies.com')
password_box.send_keys('yourpassword')

login_button = driver.find_element_by_name('commit')
login_button.click()

work_record = driver.find_element_by_link_text('勤怠')
work_record.click()
time.sleep(2)


def click_wait_appear(by, value, condition_by, condition_value, timeout=10):
    wait(driver, timeout).until(EC.element_to_be_clickable((by, value))).click()
    wait(driver, timeout).until(EC.invisibility_of_element_located((condition_by, condition_value)))


def click_wait_disappear(by, value, condition_by, condition_value, timeout=10):
    wait(driver, timeout).until(EC.element_to_be_clickable((by, value))).click()
    wait(driver, timeout).until_not(EC.invisibility_of_element_located((condition_by, condition_value)))


while True:
    try:
        day = driver.find_element_by_xpath(
            '//table[@class="employee-work-record-calendar"]'
            '//td[@class="day" and not(@class="out-of-range") and not(@class="prescribed-holiday")]'
        )
    except sce.NoSuchElementException:
        break
    action = ac.ActionChains(driver)
    action.move_to_element(day)
    action.click(day)
    action.perform()
    wait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'base-modal__content-layout')))
    checkbox = driver.find_element_by_name('editNext')
    checkbox.click()
    save_button = driver.find_element_by_xpath(
        '//button[@class="work-record-edit-modal__footer-control sw-button-primary"]')
    save_button.click()

    wait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'base-modal__content-layout')))
    wait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'ReactModalPortal')))
