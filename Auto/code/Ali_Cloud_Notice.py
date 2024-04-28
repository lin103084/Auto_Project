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

    
#GUI是否啟用
gui_list = [i for i in range(1, 3)]
headless = 2
#是否開啟GUI
# while True:
#     headless = int(input('\n請選擇是否隱藏GUI?\n1.是   2否 : '))
#     if headless in gui_list:
#         break
#     else:
#         print('輸入錯誤，重新輸入')

#Product Choose
product_dic = {"1" : "Prod1", "2" : "Prod2", "3":"Worker7"}
while True:
    product_temp = input('\n請選擇產品\n1.Prod1\n2.Prod\n3.Worker7\n選擇 : ')
    if product_temp in product_dic:break 
    else:print("\n請輸入阿拉伯數字!!!!!!!!!!!!!!!!!!!!!!")    
product = product_dic[product_temp]
#===========================================================================================================================================================
#===========================================================================================================================================================
# init WebDriver
def web_start():
    global driver
    global action
    service = Service(executable_path = "chromedriver")
    driver = webdriver.Chrome(service=service, 
    options=use_selenium_anti_reptitle.chrome_options_fun(headless))
    action = ActionChains(driver)
    #反爬處理 #降低反爬偵測機率
    stealth(driver,languages=["zh-TW", "en"], vendor="Google Inc.", platform="Win32", webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True,)
    with open('./anti_crawler_document/stealth.min.js') as f:driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": f.read()})
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """Object.defineProperty(navigator, 'webdriver', { get: () => undefined})"""})                                                             
#===========================================================================================================================================================
#===========================================================================================================================================================

#   Login
def login(account, password):
    try:
        #Open Target URL
        driver.get("https://signin.alibabacloud.com/5809754832049471.onaliyun.com/login.htm?callback=https%3A%2F%2Fnotifications-intl.console.aliyun.com%2F%3Fspm%3D5176.rocketmq.top-nav.dnews.248c7d10qmk8Oh%23%2FinnerMsg%2Funread%2F0#/main")
        driver.implicitly_wait(10)
        #driver.maximize_window()
        #Input Account
        
            #check_slider("On Try", "Account")
        input_account(account)
        check_slider("Under Try", "Account")
        # except:
        #     check_slider("On Except", "Account")
        #     input_account(account)
        #     check_slider("Under Except", "Account")

        #Input Password
        # try:
        check_slider("On Try", "Password")
        input_password(password)
        check_slider("Under Try", "Password")
        print("Input Password Finally")
        # except:
        #     check_slider("On Except", "Password")
        #     input_password(password)            
        #     check_slider("Under Except", "Password")
        #     print(">>>>>>>>>>>>>>>>>>>> Input Password Finally <<<<<<<<<<<<<<<<<<<")

    except:
        restart_browser()


#   Account Input
def input_account(account):
    print('                   Waiting For Input Account                   ')
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, 'loginName')))
    #time.sleep(random.randint(1, 3))
    account_input = driver.find_element(By.ID, 'loginName')
    action.move_to_element(account_input)
    action.click(account_input).perform()
    account_input.send_keys(Keys.CONTROL + 'a')
    account_input.send_keys(Keys.DELETE)
    #time.sleep(random.randint(1, 3))
    print('                   Input Account                   ')
    for i in account:
        account_input.send_keys(i)
        #time.sleep(random.random())    
    # account_input.send_keys(Keys.RETURN)
    next_button = driver.find_element(By.CSS_SELECTOR, ".next-col.next-col-bottom.sc-kbhJrz.iVxoQq button")
    action.move_to_element(next_button).click().perform()

#   Password Input
def input_password(password):
    print('                   Waiting For Input Password                   ')
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, 'loginPassword')))
    #time.sleep(random.randint(1, 3))
    password_input = driver.find_element(By.ID, 'loginPassword')
    password_input.send_keys(Keys.CONTROL + 'a')
    password_input.send_keys(Keys.DELETE)
    #time.sleep(random.randint(1, 3))
    
    print('                   Input Passwor                   ')
    for i in password:
        password_input.send_keys(i)
        #time.sleep(random.random())
    #password_input.send_keys(Keys.RETURN)
    login_button = driver.find_element(By.CSS_SELECTOR, ".next-col.next-col-bottom.sc-kbhJrz.iVxoQq button")
    action.move_to_element(login_button).click().perform()

#===========================================================================================================================================================
#   check Slider
def check_slider(location, status):
    print(f'>>>>>>>>>>  >>>>>>>>>>  {location} Check {status}')
    try:
        print('>>>>>>>>>>  >>>>>>>>>>  Waiting Display Slider , Switch To Ifram ')
        iframe = driver.find_element(By.ID, 'baxia-dialog-content')
        driver.switch_to.frame(iframe)

        print('>>>>>>>>>>  >>>>>>>>>>  Pause For Five Seconds Check Slider    ')
        slider = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'nc_1_n1z')))
        slider = driver.find_element(By.ID, 'nc_1_n1z')
        print('>>>>>>>>>>  >>>>>>>>>>  Display Slider!')
        
        #Loop Handle
        handle_slider_until_success(slider)
        

        print('>>>>>>>>>> >>>>>>>>>>  Slider Handle Sussful!  Change To Defaul File ')
        driver.switch_to.default_content()

    except:
        print('>>>>>>>>>>  >>>>>>>>>>  No Display Slider! Change To Defaul File ')
        driver.switch_to.default_content() 

#   handle_slider_until_success
def handle_slider_until_success(slider):
    while True:
        try:
            print("====================             Handle Slider Ing             ====================")
            handle_slider()
            
            #print('==================== Mabe Ready To Break~??? Waiting 5 Seconds ====================')                            
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.product-nav-list')))

            print('Break Loop!')
            break  
        except:
            print('====================           Handle Failed Try Again         ====================')
            #WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.product-nav-list')))
            error_message()
            # 在這裡可以進行相應的處理，例如重新取得 slider 元素

#   handle_slider
def handle_slider():
    slider = driver.find_element(By.ID, 'nc_1_n1z')
    # try:
    #print('start Debug ing!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    total_number = 420
    number_count = 20
    random_numbers = generate_random_numbers(total_number, number_count)
    print(f'有效滑動數字 : {random_numbers}')
    temp = 0
    #模擬滑動操作
    for step in random_numbers[:3]:
        action.click_and_hold(slider).move_by_offset(step, 0).perform()
        temp += 1
        print(f"{temp} / {len(random_numbers)}")
        time.sleep(random.uniform(0.1, 0.3))  # 暫停 0.1 秒

    action.release().perform()
    print(f"{temp} / {len(random_numbers)}")

    # except:
        # print('Error Click error_message')
        # error_message()

def error_message():
    error_message = driver.find_element(By.CSS_SELECTOR, ".errloading .nc_iconfont.icon_warn")
    action.move_to_element(error_message).click().perform()

        
#===========================================================================================================================================================
#隨機生成slider軌跡
def generate_random_numbers(total, count):
    # 生成count個隨機整數，總和等於total
    numbers = random.sample(range(1, total), count - 1)
    numbers.sort(reverse=True)  # 將數字排序，以確保總和的隨機性
    # 計算每個數字之間的差異，即每個部分的大小
    differences = [numbers[0]] + [numbers[i] - numbers[i-1] for i in range(1, count - 1)] + [total - numbers[-1]]
    differences.sort(reverse=True)
    return differences
#===========================================================================================================================================================
# Restart Browser
def restart_browser():
    driver.quit()
    driver.close()
    web_start()
    # service.start()
    # driver = webdriver.Chrome(service=service)
    login(account, password)  # 確保重新啟動後進行重新登入

# Crawler Data
def crawlr_and_send_data():
    try:
        driver.get("https://notifications-intl.console.aliyun.com/?spm=5176.2020520130.top-nav.dnews.29713db5iXspjW#/innerMsg/all/0")
        tbody = driver.find_element(By.TAG_NAME, 'tbody')
        elements = tbody.find_elements(By.CSS_SELECTOR, ".ng-scope")

        elements_list = []
        for i in elements:
            temp_list = []
            for j in i.find_elements(By.TAG_NAME, "td")[2:]:
                temp_list.append(j.text)
            elements_list.append(temp_list)
        elements_list = [item for item in elements_list if len(item) > 0]
        
        filter_True_data = ''
        filter_False_data = ''

        # Data
        data = elements_list
        # Current Data
        current_datetime = datetime.now()
        # 將起始時間設定為當前時間的整點
        start_datetime = current_datetime.replace(minute=0, second=0, microsecond=0)
        # 轉換每條資料的時間，並進行比對
        for item in data:
            # 確保列表至少有兩個元素
            if len(item) >= 2:
                item_datetime = datetime.strptime(item[1], "%Y-%m-%d %H:%M:%S")
                # 檢查是否在起始時間到目前時間的範圍內
                if start_datetime <= item_datetime <= current_datetime:
                    #print(f"符合條件的資料：{item}")
                    for i in item:
                        filter_True_data += f'{i} :'
                    filter_True_data = filter_True_data[:-2]
                    filter_True_data += "\n\n"

                else:
                    #print(f"不符合條件的資料：{item}")
                    for i in item:
                        filter_False_data += f'{i} :'
                    filter_False_data = filter_False_data[:-2]
                    filter_False_data += "\n\n"

            else:
                print(f"這條資料缺少時間戳記：{item}")
        

        # 使用 Telegram API 或其他方式傳送資料
        send_false_to_telegram(filter_False_data)
        send_true_to_telegram(filter_True_data)
        print('訊息發送成功!')
        


    except:
        # 登入狀態異常，重新啟動瀏覽器並重新登入
        restart_browser()

# Sent True  Message Telegram
def send_true_to_telegram(message):
    telegram_api_url = f"https://api.telegram.org/bot{telegrame_information.bot_token}/sendMessage"
    chat_id = telegrame_information.chat_id
    params = {"chat_id": chat_id, "text": f"{product} - 符合條件的資料：\n{message}\n\n\n\n\n"}
    requests.post(telegram_api_url, params=params)

# Sent False  Message Telegram
def send_false_to_telegram(message):
    telegram_api_url = f"https://api.telegram.org/bot{telegrame_information.bot_token}/sendMessage"
    chat_id = telegrame_information.chat_id
    params = {"chat_id": chat_id, "text": f"{product} - 不符合條件的資料：\n{message}"}
    requests.post(telegram_api_url, params=params)


# schedule job
def schedule_job():
    # 每個整點執行一次
    schedule.every().hour.at(":00").do(crawlr_and_send_data)
    #schedule.every().day.at("21:00:00").do(crawlr_and_send_data)  #1
    while True:
        schedule.run_pending()
        time.sleep(1)


#===========================================================================================================================================================
#===========================================================================================================================================================
# Main Program
if __name__ == "__main__":
    web_start()
    #Set user password
    if product == "Prod1":
        account = "account1.onaliyun.com"
        password = "12345678"
    elif product == "Prod2":  
        account = "account2.onaliyun.com"
        password = "12345678"
    elif product == "Worker7":
        account = "Worker7.onaliyun.com"
        password = "12345678"
    #Login
    login(account, password)
    #Sent message
    schedule_job()

    