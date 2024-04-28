from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service 

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
import schedule
import time
import random
import threading
from datetime import datetime

#Mypackage
from selenium_stealth import stealth
from mypackage import use_selenium_anti_reptitle
import mypackage.telegrame_information_Ali_Notify_bot as telegrame_information
from mypackage import sent_telegram_bot
from mypackage import login_password

LOGINPASSWORD = login_password.PASSWORD
while True:
    answer = input("請輸入密碼:")
    if answer == LOGINPASSWORD:
        break
    print("輸入錯誤")

def mustang_balance(url, account, password):
    web_start()
    driver.get(url)
    driver.implicitly_wait(10)
    
    #Account
    account_input = driver.find_element(By.ID, 'name')
    action.move_to_element(account_input)
    action.click(account_input).perform()
    account_input.send_keys(Keys.CONTROL + 'a')
    account_input.send_keys(Keys.DELETE)
    for i in account:account_input.send_keys(i)

    #password
    password_input = driver.find_element(By.ID, 'password')
    action.move_to_element(password_input)
    action.click(password_input).perform()
    password_input.send_keys(Keys.CONTROL + 'a')
    password_input.send_keys(Keys.DELETE)
    for i in password:password_input.send_keys(i)

    #Login 
    login_button = driver.find_element(By.ID, "enter")
    action.move_to_element(login_button).click().perform()

    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "tr>td.nowrap+td>pre")))
    mustang_balance = driver.find_element(By.CSS_SELECTOR, "tr>td.nowrap+td>pre").text
    # # 遍歷父層元素，取得文字內容
    # for parent_element in parent_elements:
    #     date_text = parent_element.find_elements("td.nowrap").text
    #     number_text = parent_element.text
    # print(f"日期: {date_text}, 數字: {number_text}")
    print(mustang_balance)




def ali_balance(url, account, password):
    web_start()
    
    
    #Account
    account_input = driver.find_element(By.ID, 'name')
    action.move_to_element(account_input)
    action.click(account_input).perform()
    account_input.send_keys(Keys.CONTROL + 'a')
    account_input.send_keys(Keys.DELETE)
    for i in account:account_input.send_keys(i)

    #password
    password_input = driver.find_element(By.ID, 'password')
    action.move_to_element(password_input)
    action.click(password_input).perform()
    password_input.send_keys(Keys.CONTROL + 'a')
    password_input.send_keys(Keys.DELETE)
    for i in password:password_input.send_keys(i)

    #Login 
    login_button = driver.find_element(By.ID, "enter")
    action.move_to_element(login_button).click().perform()




#===========================================================================================================================================================
#===========================================================================================================================================================
def web_start():
    global driver
    global action
    service = Service(executable_path = "chromedriver")
    driver = webdriver.Chrome(service=service, 
    options=use_selenium_anti_reptitle.chrome_options_fun(2))
    action = ActionChains(driver)
    #反爬處理 #降低反爬偵測機率
    stealth(driver,languages=["zh-TW", "en"], vendor="Google Inc.", platform="Win32", webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True,)
    with open('./anti_crawler_document/stealth.min.js') as f:driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": f.read()})
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """Object.defineProperty(navigator, 'webdriver', { get: () => undefined})"""})                                                             




if __name__ == "__main__":
    ali_url = "https://signin-intl.aliyun.com/login.htm#/main"
    ali_account = "accupnt..onaliyun.com"
    ali_password = "12345678"
    ali_balance(ali_url, ali_account, ali_password)
