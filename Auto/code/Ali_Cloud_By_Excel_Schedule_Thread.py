from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
#Anti-crawler
from selenium_stealth import stealth

import time
import os
import openpyxl
import threading
import schedule
import random

#write package by me
from mypackage import use_wait_method as wait
from mypackage import use_readfile
from mypackage import use_selenium_anti_reptitle
from mypackage import sent_telegram_bot
from mypackage import login_password

LOGINPASSWORD = login_password.PASSWORD
while True:
    answer = input("請輸入密碼:")
    if answer == LOGINPASSWORD:
        break
    print("輸入錯誤")
#更改路徑  讓檔案產生在上上層
path = '../' 
os.chdir(path=path)
os.chdir(path=path)
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#Product choose
product_dic = {"1" : "200", "2" : "401"}
while True:
    product_temp = input('\n請選擇正常狀態\n1.狀態:200  = 正常\n2.狀態:401  = 正常\n產品選擇 : ')

    if product_temp in product_dic:
        break
    else:
        print("\n請輸入阿拉伯數字!!!!!!!!!!!!!!!!!!!!!!")
        
product = product_dic[product_temp]

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#線程數量
thread_count_list = [str(i) for i in range(1, 13)]
while True:
    try:
        thread_question = input('\n請輸入開啟線程數量 \n最小1 ~ 最大 12 \n線程數量 : ')
        if thread_question in thread_count_list:
            thread_count = int(thread_question)
            break

        elif thread_question == "+":
            thread_count = int(input("\n請輸入解放的線呈數量 : "))
            break
        
        else:
            print('\n輸入超出範圍，重新輸入\n')

    except:
         print('\n\n輸入錯誤，重新輸入')
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#GUI是否啟用
gui_list = [i for i in range(1, 3)]
#是否開啟GUI
while True:
    headless = int(input('\n請選擇是否隱藏GUI?\n1.是   2否 : '))
    if headless in gui_list:
        break
    else:
        print('輸入錯誤，重新輸入')
print()
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#導入Dns資料
domain_excel = use_readfile.excel_file()
#為了要重複執行，必須把消耗過後的先複製一份，最後再替補回來，持續使用
domain_excel_repeat = domain_excel.copy()

#計算Domain總數量
domain_excel_len = len(domain_excel)

#Domain檢測計次
count = 0

#判斷是否為主要的封禁Dns結果 
finally_title_domain_result = []


def job():
    global count
    global finally_title_domain_result
    global domain_excel
    global domain_excel_repeat

    #程式開始執行時間
    program_start_localtime = time.localtime()
    program_start_localtime_result = time.strftime("%Y-%m-%d %I:%M:%S %p", program_start_localtime)
    program_start_time = time.time()

    start_wb_name_localtime = time.localtime()  
    start_wb_name_localtime = time.strftime("%Y%m%d_%H_%M_%S", start_wb_name_localtime)

    def crawler():
        global count
        global finally_title_domain_result
        global domain_excel
        global domain_excel_repeat

        while domain_excel:
            try:
                service = Service(executable_path = "chromedriver")
                #webdriver 改用自動新driver + 隱藏網頁參數
                wd = webdriver.Chrome(service=service, 
                options=use_selenium_anti_reptitle.chrome_options_fun(headless))

                #反爬處理 #降低反爬偵測機率
                stealth(wd,languages=["zh-TW", "en"],vendor="Google Inc.",platform="Win32",webgl_vendor="Intel Inc.",renderer="Intel Iris OpenGL Engine",fix_hairline=True,)
                wd.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """Object.defineProperty(navigator, 'webdriver', { get: () => undefined})"""})


                #目標網址
                wd.get('https://zijian.aliyun.com/detect/http')

                #等待網頁正常
                wd.implicitly_wait(10)

                '''左側搜尋欄  運營商 / 地區'''
                #Search Tag
                search_tag = wd.find_element(By.CSS_SELECTOR, '.input-select') 
                search_tag.click()

                #左側欄位
                search_tags_form = wd.find_element(By.CSS_SELECTOR, '.isp-and-city').find_element(By.CSS_SELECTOR, '.next-form.next-medium').find_elements(By.CSS_SELECTOR, '.next-row')

                #operator排除四個營運商 阿里雲 / 微軟 / 谷哥 / 亞馬遜
                operator = search_tags_form[0].find_element(By.CSS_SELECTOR, '.next-checkbox-group.next-checkbox-group-hoz.checkbox-group').find_elements(By.CSS_SELECTOR, '.next-checkbox-wrapper')
                
                search_tag_ali = operator[0].find_element(By.CSS_SELECTOR, '.next-checkbox')
                search_tag_ms = operator[4].find_element(By.CSS_SELECTOR, '.next-checkbox')
                search_tag_google = operator[5].find_element(By.CSS_SELECTOR, '.next-checkbox')
                search_tag_aws = operator[6].find_element(By.CSS_SELECTOR, '.next-checkbox')

                #operator排除四個營運商 阿里雲 / 微軟 / 谷哥 / 亞馬遜
                time.sleep(2) #緩衝一下，不然提交太快，有勾等於沒勾選
                search_tag_ali.click()
                search_tag_ms.click()
                search_tag_google.click()
                search_tag_aws.click()
                time.sleep(2)
                
                '''Domain檢測'''
                while domain_excel:
                    try:
                        #成功取出最後一個domain 進行檢測 不成功就從except塞回去
                        domain = domain_excel.pop()
                        #計算目前 domain 檢測進度
                        count += 1

                        #暫時用來存結果的，每次新進來都會清空
                        temp_repeat_domain_result = []

                        #暫時存取share_link
                        share_link_temp = []

                        #系統當下時間            
                        localtime = time.localtime()
                        localtime_result = time.strftime("%Y-%m-%d %p %I:%M:%S", localtime)
                        print(f"阿里雲檢測: {domain} 中... {count} / {domain_excel_len}   ---   LocalTime:{localtime_result}")

                        #Search Input
                        search_input = wd.find_element(By.ID, 'url1')
                        search_input.send_keys(Keys.CONTROL + 'a')
                        search_input.send_keys(Keys.DELETE)
                        search_input.send_keys(domain)
                        search_input.send_keys(Keys.RETURN)       

                        #此Try 處理阿里雲loading
                        try:
                            #等loading消失 最多等100秒
                            wait.use_wait_not_visible(wd, By.CSS_SELECTOR, '.next-loading-tip-content', 100)

                            #等待資料表格是否正常出現
                            wait.use_wait_visible(wd, By.TAG_NAME, 'tbody', 3)

                            #資料擷取    
                            try:                  
                                #等待share-link出現
                                wait.use_wait_visible_keyword(wd, By.CSS_SELECTOR, '.share-link', 'https://boce.aliyun.com', 150)
                                
                                #等待 是否有超時 出現(阿里雲Http二次請求)
                                wait.use_wait_visible_keyword(wd, By.TAG_NAME, 'tbody', '610', 30)
                            
                                #點一下 狀態 排列
                                #status_down = wd.find_elements(By.CSS_SELECTOR, '.next-table-cell.next-table-header-node')[2].find_element(By.CSS_SELECTOR, '.next-table-sort.next-table-header-icon')
                                #status_down.click()

                                #2023/02/15改版，更強的反爬     
                                #最下面的資料 用鍵盤往下        
                                actions = ActionChains(wd)
                                tag = wd.find_element(By.CSS_SELECTOR, '.next-table-row.last')
                                actions.move_to_element(tag)
                                actions.click(tag)

                                #讓頁面往下
                                for w in range(1, 101):                       
                                    if w <= 1 or w % 5 == 0:
                                        time.sleep(2)
                                        #整份檢測結果表單
                                        tbody = wd.find_element(By.TAG_NAME, 'tbody').find_elements(By.CSS_SELECTOR, '.next-table-row')
                                        
                                        #探測點
                                        title_list = [i.find_elements(By.CSS_SELECTOR, '.next-table-cell')[0].text for i in tbody]

                                        #ip
                                        ip_list = [i.find_elements(By.CSS_SELECTOR, '.next-table-cell')[1].text for i in tbody]

                                        #狀態             
                                        status_list = [i.find_elements(By.CSS_SELECTOR, '.next-table-cell')[2].text for i in tbody]

                                        #分享連結
                                        share_link = wd.find_element(By.CSS_SELECTOR, '.share-link').text     
                                        #share_link會有抓空的問題，有抓到就先存起來
                                        if share_link not in share_link_temp:
                                            share_link_temp.append(share_link)

                                        #整理上面結果
                                        title_and_result_list = [[title, ip, status] for title, ip, status in zip(title_list, ip_list, status_list)]
                                                            
                                        #篩選判斷
                                        #Product choose
                                        if product == "200":
                                            for i in title_and_result_list:
                                                if i[0] in [i[1] for i in temp_repeat_domain_result]:
                                                    continue
                                                elif i[2][:3] != '200':                                 
                                                    if i[2] == 'dns错误': #12/23後應該沒了
                                                        i[1] ='N/A'
                                                    elif i[2] == '613': #12/23新增條件 應該是之前的dns錯誤
                                                        i[1] ='N/A'
                                                    elif i[1] == '': #若IP為空值
                                                        i[1] ='N/A'
                                                    # elif i[0] == '北京北京电信':
                                                    #     i[1] ='★'
                                                    #     i[2] ='★'
                                                    temp_repeat_domain_result.append([domain, i[0], i[1], i[2], share_link_temp[0]])

                                        elif product == "401":
                                            for i in title_and_result_list:
                                                if i[0] in [i[1] for i in temp_repeat_domain_result]:
                                                    continue
                                                elif i[2][:3] != '401':                                 
                                                    if i[2] == 'dns错误': #12/23後應該沒了
                                                        i[1] ='N/A'
                                                    elif i[2] == '613': #12/23新增條件 應該是之前的dns錯誤
                                                        i[1] ='N/A'
                                                    elif i[1] == '': #若IP為空值
                                                        i[1] ='N/A'
                                                    # elif i[0] == '北京北京电信':
                                                    #     i[1] ='★'
                                                    #     i[2] ='★'
                                                    temp_repeat_domain_result.append([domain, i[0], i[1], i[2], share_link_temp[0]])
                                
                                    #往下10筆 就開始撈資料
                                    actions.key_down(Keys.DOWN)
                                    actions.perform()
                                                                
                                #檢測狀態如果都是200沒有問題的話，放入空值外加一枚連結
                                temp_count = 0
                                for j in temp_repeat_domain_result:
                                    if domain in j[0]:
                                        temp_count += 1

                                if temp_count == 0:
                                    temp_repeat_domain_result.append([domain, "", "", "", share_link_temp[0]])      



                            except:
                                #點一下 狀態 排列
                                #status_down = wd.find_elements(By.CSS_SELECTOR, '.next-table-cell.next-table-header-node')[2].find_element(By.CSS_SELECTOR, '.next-table-sort.next-table-header-icon')
                                #status_down.click()

                                #2023/02/15改版，更強的反爬     
                                #最下面的資料 用鍵盤往下        
                                actions = ActionChains(wd)
                                tag = wd.find_element(By.CSS_SELECTOR, '.next-table-row.last')
                                actions.move_to_element(tag)
                                actions.click(tag)

                                #讓頁面往下
                                for w in range(1, 101):                       
                                    if w <= 1 or w % 5 == 0:
                                        time.sleep(2)
                                        #整份檢測結果表單
                                        tbody = wd.find_element(By.TAG_NAME, 'tbody').find_elements(By.CSS_SELECTOR, '.next-table-row')
                                        
                                        #探測點
                                        title_list = [i.find_elements(By.CSS_SELECTOR, '.next-table-cell')[0].text for i in tbody]

                                        #ip
                                        ip_list = [i.find_elements(By.CSS_SELECTOR, '.next-table-cell')[1].text for i in tbody]

                                        #狀態             
                                        status_list = [i.find_elements(By.CSS_SELECTOR, '.next-table-cell')[2].text for i in tbody]

                                        #分享連結
                                        share_link = wd.find_element(By.CSS_SELECTOR, '.share-link').text        
                                        #share_link會有抓空的問題，有抓到就先存起來
                                        if share_link not in share_link_temp:
                                            share_link_temp.append(share_link)

                                        #整理上面結果
                                        title_and_result_list = [[title, ip, status] for title, ip, status in zip(title_list, ip_list, status_list)]
                                                            
                                        #篩選判斷
                                        #Product choose
                                        if product == "200":
                                            for i in title_and_result_list:
                                                if i[0] in [i[1] for i in temp_repeat_domain_result]:
                                                    continue
                                                elif i[2][:3] != '200':                                 
                                                    if i[2] == 'dns错误': #12/23後應該沒了
                                                        i[1] ='N/A'
                                                    elif i[2] == '613': #12/23新增條件 應該是之前的dns錯誤
                                                        i[1] ='N/A'
                                                    elif i[1] == '': #若IP為空值
                                                        i[1] ='N/A'
                                                    # elif i[0] == '北京北京电信':
                                                    #     i[1] ='★'
                                                    #     i[2] ='★'
                                                    temp_repeat_domain_result.append([domain, i[0], i[1], i[2], share_link_temp[0]])

                                        elif product == "401":
                                            for i in title_and_result_list:
                                                if i[0] in [i[1] for i in temp_repeat_domain_result]:
                                                    continue
                                                elif i[2][:3] != '401':                                 
                                                    if i[2] == 'dns错误': #12/23後應該沒了
                                                        i[1] ='N/A'
                                                    elif i[2] == '613': #12/23新增條件 應該是之前的dns錯誤
                                                        i[1] ='N/A'
                                                    elif i[1] == '': #若IP為空值
                                                        i[1] ='N/A'
                                                    # elif i[0] == '北京北京电信':
                                                    #     i[1] ='★'
                                                    #     i[2] ='★'
                                                    temp_repeat_domain_result.append([domain, i[0], i[1], i[2], share_link_temp[0]])
                                
                                    #往下10筆 就開始撈資料
                                    actions.key_down(Keys.DOWN)
                                    actions.perform()
                                                                
                                #檢測狀態如果都是200沒有問題的話，放入空值外加一枚連結
                                temp_count = 0
                                for j in temp_repeat_domain_result:
                                    if domain in j[0]:
                                        temp_count += 1

                                if temp_count == 0:
                                    temp_repeat_domain_result.append([domain, "", "", "", share_link_temp[0]])      

                        

                        except:
                            #成功取出最後一個domain 進行檢測 不成功就從except塞回去
                            domain_excel.append(domain)
                            #計算目前 domain 檢測進度
                            count -= 1

                            #當下時間實體化
                            loadong_localtime = time.localtime()
                            loadong_localtime_result = time.strftime("%Y-%m-%d %I:%M:%S %p", loadong_localtime)
                            print(f"檢測:{domain} 時，資料載入不完全，Loading時間過長, or 資料表格無正常出現")
                            print(f"\nLocaltime: {loadong_localtime_result} --- 將於1秒後重新啟動Chrome! 請稍後") 
                            wd.close()
                            wd.quit()

                            print('Chrome重新啟動中...')
                            break


                    except:
                        #成功取出最後一個domain 進行檢測 不成功就從except塞回去
                        domain_excel.append(domain)
                        #計算目前 domain 檢測進度
                        count -= 1
                        break
                    
                    finally:
                        for i in temp_repeat_domain_result:
                            finally_title_domain_result.append(i)



            #第一層 except 負責關閉 Chrome 重啟使用
            except:
                #當下時間實體化
                error_localtime = time.localtime()
                error_localtime_result = time.strftime("%Y-%m-%d %I:%M:%S %p", error_localtime)
                print(f"\nLocaltime: {error_localtime_result} --- 不知名錯誤，重新啟動Chrome! 請稍後'") 
                wd.close()
                wd.quit()
                print('Chrome重新啟動中...')

    # 創建線程並加入至線程列表
    threads = []
    for q in range(thread_count):
        thread = threading.Thread(target=crawler)
        thread.start()
        threads.append(thread)

    # 等待所有線程完成
    for thread in threads:
        thread.join()
        

    #程式結束執行時間
    program_end_localtime = time.localtime()
    program_end_localtime_result = time.strftime("%Y-%m-%d %I:%M:%S %p", program_end_localtime)
    program_end_time = time.time()

    program_run_time = round(program_end_time - program_start_time)
    hour = program_run_time // 3600
    minute = (program_run_time - 3600 * hour) // 60
    second = program_run_time - 3600 * hour - 60 * minute

    end_wb_name_localtime = time.localtime()  
    end_wb_name_localtime = time.strftime("%H_%M_%S", end_wb_name_localtime)


    #建立Excel
    wb = openpyxl.Workbook()    # 建立空白的 Excel 活頁簿物件
    s1 = wb.active
    title = ['域名', '探測點', 'IP', '狀態', '分享連結']
    s1.append(title)

    #彙整到Excel
    for k in finally_title_domain_result:
            s1.append(k)

    #創建隨機數，讓檔案生成時不會重複
    random_int = str(round(random.randint(0, 10000), 3))
    wb.save(start_wb_name_localtime + '__' + end_wb_name_localtime + '__' + random_int + '.xlsx')


    #結束檢測，關閉視窗。
    print(f'域名已全數檢測完畢!\n開始時間: {program_start_localtime_result}\n結束時間: {program_end_localtime_result}\n總計時間: {hour}:{minute}:{second}')


    #讓下一次可以重新執行
    count = 0
    finally_title_domain_result = []
    domain_excel = domain_excel_repeat.copy()







schedule.every().day.at("00:45:00").do(job)  #1
schedule.every().day.at("01:45:00").do(job)  #2
schedule.every().day.at("02:45:00").do(job)  #3
schedule.every().day.at("03:45:00").do(job)  #4
schedule.every().day.at("04:45:00").do(job)  #5
schedule.every().day.at("05:45:00").do(job)  #6

# schedule.every().day.at("06:45:00").do(job)  #7
# schedule.every().day.at("07:45:00").do(job)  #8
# schedule.every().day.at("08:45:00").do(job)  #9
# schedule.every().day.at("09:45:00").do(job)  #10
# schedule.every().day.at("10:45:00").do(job)  #11
# schedule.every().day.at("11:45:00").do(job)  #12

# schedule.every().day.at("12:45:00").do(job)  #13
# schedule.every().day.at("13:45:00").do(job)  #14
# schedule.every().day.at("14:45:00").do(job)  #15
schedule.every().day.at("15:45:00").do(job)  #16
schedule.every().day.at("16:45:00").do(job)  #17
schedule.every().day.at("17:45:00").do(job)  #18

schedule.every().day.at("18:45:00").do(job)  #19
schedule.every().day.at("19:45:00").do(job)  #20
schedule.every().day.at("20:45:00").do(job)  #21
schedule.every().day.at("21:45:00").do(job)  #22
schedule.every().day.at("22:45:00").do(job)  #23
schedule.every().day.at("23:45:00").do(job)  #00




while True:  
  schedule.run_pending() 
  time.sleep(1)  