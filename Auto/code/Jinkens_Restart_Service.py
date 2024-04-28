from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Mypackage
from selenium_stealth import stealth
from mypackage import use_selenium_anti_reptitle
import mypackage.telegrame_information_Ali_Notify_bot as telegrame_information
from mypackage import sent_telegram_bot

import threading
import schedule
import time
from mypackage import login_password

LOGINPASSWORD = login_password.PASSWORD
while True:
    answer = input("請輸入密碼:")
    if answer == LOGINPASSWORD:
        break
    print("輸入錯誤")



def web_start():
    service = Service(executable_path = "chromedriver")
    driver = webdriver.Chrome(service=service, 
    options=use_selenium_anti_reptitle.chrome_options_fun(2))
    #反爬處理 #降低反爬偵測機率
    stealth(driver,languages=["zh-TW", "en"], vendor="Google Inc.", platform="Win32", webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True,)
    with open('./anti_crawler_document/stealth.min.js') as f:driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": f.read()})
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """Object.defineProperty(navigator, 'webdriver', { get: () => undefined})"""})    
    return driver

def login(url, return_driver):
    account = 'account'
    password = '12345678'
    return_driver.get(url)

    #account password input
    input_account(account, return_driver)
    input_password(password, return_driver)
    time.sleep(5)

def input_account(account, return_driver):
    WebDriverWait(return_driver, 3).until(EC.element_to_be_clickable((By.ID, 'j_username')))
    account_input = return_driver.find_element(By.ID, 'j_username')
    account_input.click()
    account_input.send_keys(Keys.CONTROL + 'a')
    account_input.send_keys(Keys.DELETE)
    for i in account:account_input.send_keys(i)
    password = return_driver.find_element(By.XPATH, '/html/body/div/div/form/div[2]/input')
    password.click()

def input_password(password, return_driver):
    password_input = return_driver.find_element(By.XPATH, '/html/body/div/div/form/div[2]/input')
    password_input.click()
    password_input.send_keys(Keys.CONTROL + 'a')
    password_input.send_keys(Keys.DELETE)
    for i in password:password_input.send_keys(i)
    login_button = return_driver.find_element(By.XPATH, "/html/body/div/div/form/div[3]/input")
    login_button.click()



def start_thread(selected_value):
    # 啟動線程    # 創建一個執行任務的線程
    task_thread = threading.Thread(target=job_scheduler, args=(selected_value,))
    task_thread.start()

def job_scheduler(selected_value):
    return_driver = web_start()
    login(url, return_driver)

    #Loop schedule
    schedule.every(3).minutes.do(restart_server, selected_value, return_driver)
  

def restart_server(selected_value, return_driver):
    select_server_button = return_driver.find_element(By.ID, "main-panel").find_element(By.NAME, "parameter").find_element(By.NAME, "value")
    select = Select(select_server_button)
    select.select_by_value(selected_value)
    time.sleep(3)
    return_driver.find_element(By.ID, "yui-gen1-button").click()    
    print(f"{selected_value} 建置成功!")
    currentTime = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime())
    print(f"當前時間 : {currentTime}")
    time.sleep(3)
    return_driver.get(url)



    


if __name__ == "__main__":
    url = "https://jks.w2e4ms.com"
    dropdown_list = ["app-02", "app-03", "app-04", "app-05", "app-07", "app-08"]


    for selected_value in dropdown_list:
        print(f"成功啟動 : {selected_value}")
        start_thread(selected_value)
        time.sleep(1)

    while True:
        schedule.run_pending()
        time.sleep(1)