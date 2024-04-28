from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
#Anti-crawler
from selenium_stealth import stealth

import time
# import os
# import openpyxl
import threading

#write package by me
from mypackage import use_wait_method as wait
from mypackage import use_readfile
from mypackage import use_selenium_anti_reptitle
from mypackage import use_google_form
from mypackage import sent_telegram_bot
from mypackage import login_password

LOGINPASSWORD = login_password.PASSWORD
while True:
    answer = input("請輸入密碼:")
    if answer == LOGINPASSWORD:
        break
    print("輸入錯誤")

#Path change
# path = '../'  
# os.chdir(path=path)
# os.chdir(path=path)
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
#worker
work_name_dic = {
    "1" : "Worker1",
    "2" : "Worker2",
    "3" : "Worker3",
    "4" : "Worker4",
    "5" : "Worker5",
    "6" : "Worker6",
    "7" : "Worker7",
    "8" : "Worker8"
}

while True:
    work_name_temp = input('\n請選擇操作夥伴\n1.Worker1   2.Worker2   3.Worker3   4.Worker4   5.Worker5   6.Worker6   7.Worker7   8.Worker8\n當前操作夥伴 : ')

    if work_name_temp in work_name_dic:
        break
    else:
        print("\n請輸入阿拉伯數字!!!!!!!!!!!!!!!!!!!!!!")

work_name = work_name_dic[work_name_temp]
print(f'當前執行Auto夥伴: {work_name}')

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

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
choose_remove_or_add_610_dic = {
    '1': '是',
    '2': '否'
}

while True:
    remove_or_add = input('\n請選擇檢測時是否移除 狀態:610?\n1.是   2否 : ')
    if remove_or_add in choose_remove_or_add_610_dic:
        break
    else:
        print('輸入錯誤，重新輸入')

choose_remove_or_add_610 = choose_remove_or_add_610_dic[remove_or_add]

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#判斷導入資料是告警，還是恢復的CSV檔案，來源是zabbix to grfana data
alarm_or_recover_dic = {
    '1': '告警',
    '2': '恢復'
}

while True:
    alarm_or_recover = input('\n檢測資料為告警還是恢復?\n1.告警 2.恢復 : ')
    if alarm_or_recover in alarm_or_recover_dic:
        break
    else:
        print('輸入錯誤，重新輸入')

#方便提交資料時使用，恢復的部分，有恢復時間需要填寫
csv_data_type = alarm_or_recover_dic[alarm_or_recover]

#清洗完成後的資料
csv_file_temp = use_readfile.csv_file()[1:] #就是刪除title列
csv_file = []
for i in csv_file_temp:
    if len(i) != 0:
        csv_file.append(i)

#主要檢測資料
csv_data = [i[:-1] for i in csv_file]

# if csv_data_type == '告警':
#     #告警的資料做清洗
#     for i in csv_file:
#         csv_data.append(i[0:-1])

# else:
#     #恢復的資料做清洗
#     for i in csv_file:
#         i[0], i[1] = i[1], i[0]
#         csv_data.append(i[0:-2])


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#calculate detection total count
csv_data_len = len(csv_data)

#detection檢測計次
count = 0

#判斷是否為主要的封禁Dns結果
# finally_title_domain_result = []

#程式開始執行時間
program_start_localtime = time.localtime()
program_start_localtime_result = time.strftime("%Y-%m-%d %I:%M:%S %p", program_start_localtime)
program_start_time = time.time()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def crawler():
    global count
    while csv_data:
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

            time.sleep(2) #緩衝一下，不然提交太快，有勾等於沒勾選
            #operator排除四個營運商 阿里雲 / 微軟 / 谷哥 / 亞馬遜
            search_tag_ali.click()
            search_tag_ms.click()
            search_tag_google.click()
            search_tag_aws.click()
           
            
            '''Domain檢測'''
            while csv_data:
                try:
                    #成功取出最後一個domain 進行檢測 不成功就從except塞回去                    
                    detection_data = csv_data.pop()
                    #domain
                    domain = detection_data[0]
                    #time
                    domain_local_time = detection_data[1]
                    #machine
                    machine = detection_data[2]
                    #event_id
                    event_id = detection_data[4]

                    #計算目前 domain 檢測進度
                    count += 1

                    #暫時用來存結果的，每次新進來都會清空
                    temp_repeat_domain_result = []

                    #暫時存取share_link
                    share_link_temp = []

                    #系統當下時間            
                    localtime = time.localtime()
                    localtime_result = time.strftime("%Y-%m-%d %p %I:%M:%S", localtime)
                    print(f"阿里雲檢測: {domain} 中... {count} / {csv_data_len}   ---   LocalTime:{localtime_result}")

                    #Search Input
                    search_input = wd.find_element(By.ID, 'url1')
                    search_input.send_keys(Keys.CONTROL + 'a')
                    search_input.send_keys(Keys.DELETE)
                    search_input.send_keys(f'https://{domain}')
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
                                            elif choose_remove_or_add_610 == '是':#移除610的話
                                                if i[2][:3] != '200' and i[2][:3] != '610':                                 
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
                                            else:#不要移除610
                                                if i[2][:3] != '200':                                 
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
                                            elif choose_remove_or_add_610 == '是':#移除610的話
                                                if i[2][:3] != '401' and i[2][:3] != '610':                                 
                                                    if i[2] == 'dns错误': #12/23後應該沒了
                                                        i[1] ='N/A'
                                                    elif i[2] == '613': #12/23新增條件 應該是之前的dns錯誤
                                                        i[1] ='N/A'
                                                    elif i[1] == '': #若IP為空值
                                                        i[1] ='N/A'                                                    
                                                    temp_repeat_domain_result.append([domain, i[0], i[1], i[2], share_link_temp[0]])

                                            else:#不要移除610
                                                if i[2][:3] != '401':                                 
                                                    if i[2] == 'dns错误': #12/23後應該沒了
                                                        i[1] ='N/A'
                                                    elif i[2] == '613': #12/23新增條件 應該是之前的dns錯誤
                                                        i[1] ='N/A'
                                                    elif i[1] == '': #若IP為空值
                                                        i[1] ='N/A'                                                    
                                                    temp_repeat_domain_result.append([domain, i[0], i[1], i[2], share_link_temp[0]])


                                
                                #往下10筆 就開始撈資料
                                actions.key_down(Keys.DOWN)
                                actions.perform()
                                                            
                            #檢測狀態如果都是200沒有問題的話，放入空值外加一枚連結
                            temp_count = 0
                            for j in temp_repeat_domain_result:
                                if domain in j[0]:
                                    temp_count += 1

                            #整理並提交到google sheet
                            #沒有封禁的，就直接上傳
                            if temp_count == 0:
                                if csv_data_type == '告警':
                                    use_google_form.alarm_recover(domain, domain_local_time, "", machine, event_id, "", share_link_temp[0], work_name)
                                
                                #恢復的
                                else:
                                    use_google_form.alarm_recover(domain, domain_local_time, domain_local_time, machine, event_id, "", share_link_temp[0], work_name)                                   
                                

                            else:
                                update_google_sheet_title = [] #全部封禁地區

                                #[domain, 地區, IP, 狀態, share_link]
                                for k in temp_repeat_domain_result:
                                    update_google_sheet_title.append(k[1])
                                
                                #提交到google sheet
                                if csv_data_type == '告警':
                                    if len(update_google_sheet_title) >=18:
                                        use_google_form.alarm_recover(domain, domain_local_time, "", machine, event_id, '多地區', share_link_temp[0], work_name)
                                    else:
                                        use_google_form.alarm_recover(domain, domain_local_time, "", machine, event_id, update_google_sheet_title, share_link_temp[0], work_name)

                                #恢復    
                                else:
                                    if len(update_google_sheet_title) >=18:
                                        use_google_form.alarm_recover(domain, domain_local_time, domain_local_time, machine, event_id, '多地區', share_link_temp[0], work_name)          
                                    else:
                                        use_google_form.alarm_recover(domain, domain_local_time, domain_local_time, machine, event_id, update_google_sheet_title, share_link_temp[0], work_name)          

            

                            


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
                                            elif choose_remove_or_add_610 == '是':#移除610的話
                                                if i[2][:3] != '200' and i[2][:3] != '610':
                                                    if i[2] == 'dns错误': #12/23後應該沒了
                                                        i[1] ='N/A'
                                                    elif i[2] == '613': #12/23新增條件 應該是之前的dns錯誤
                                                        i[1] ='N/A'
                                                    elif i[1] == '': #若IP為空值
                                                        i[1] ='N/A'
                                                    temp_repeat_domain_result.append([domain, i[0], i[1], i[2], share_link_temp[0]])
                                            else:#不要移除610
                                                if i[2][:3] != '200':                                 
                                                    if i[2] == 'dns错误': #12/23後應該沒了
                                                        i[1] ='N/A'
                                                    elif i[2] == '613': #12/23新增條件 應該是之前的dns錯誤
                                                        i[1] ='N/A'
                                                    elif i[1] == '': #若IP為空值
                                                        i[1] ='N/A'                                                    
                                                    temp_repeat_domain_result.append([domain, i[0], i[1], i[2], share_link_temp[0]])

                                    elif product == "401":
                                         for i in title_and_result_list:
                                            if i[0] in [i[1] for i in temp_repeat_domain_result]:
                                                continue
                                            elif choose_remove_or_add_610 == '是':#移除610的話
                                                if i[2][:3] != '401' and i[2][:3] != '610':                                 
                                                    if i[2] == 'dns错误': #12/23後應該沒了
                                                        i[1] ='N/A'
                                                    elif i[2] == '613': #12/23新增條件 應該是之前的dns錯誤
                                                        i[1] ='N/A'
                                                    elif i[1] == '': #若IP為空值
                                                        i[1] ='N/A'                                                
                                                    temp_repeat_domain_result.append([domain, i[0], i[1], i[2], share_link_temp[0]])

                                            else:#不要移除610
                                                if i[2][:3] != '401':                                 
                                                    if i[2] == 'dns错误': #12/23後應該沒了
                                                        i[1] ='N/A'
                                                    elif i[2] == '613': #12/23新增條件 應該是之前的dns錯誤
                                                        i[1] ='N/A'
                                                    elif i[1] == '': #若IP為空值
                                                        i[1] ='N/A'                                                    
                                                    temp_repeat_domain_result.append([domain, i[0], i[1], i[2], share_link_temp[0]])
                            
                                #往下10筆 就開始撈資料
                                actions.key_down(Keys.DOWN)
                                actions.perform()
                                                            
                           #檢測狀態如果都是200沒有問題的話，放入空值外加一枚連結
                            temp_count = 0
                            for j in temp_repeat_domain_result:
                                if domain in j[0]:
                                    temp_count += 1

                            #整理並提交到google sheet
                            #沒有封禁的，就直接上傳
                            if temp_count == 0:
                                if csv_data_type == '告警':
                                    use_google_form.alarm_recover(domain, domain_local_time, "", machine, event_id, "", share_link_temp[0], work_name)
                                
                                #恢復的
                                else:
                                    use_google_form.alarm_recover(domain, domain_local_time, domain_local_time, machine, event_id, "", share_link_temp[0], work_name)
                                # temp_repeat_domain_result.append([domain, "", "", "", share_link])    
                                

                            else:
                                update_google_sheet_title = [] #全部封禁地區

                                #[domain, 地區, IP, 狀態, share_link]
                                for k in temp_repeat_domain_result:
                                    update_google_sheet_title.append(k[1])
                                
                                #提交到google sheet
                                if csv_data_type == '告警':
                                    if len(update_google_sheet_title) >=18:
                                        use_google_form.alarm_recover(domain, domain_local_time, "", machine, event_id, '多地區', share_link_temp[0], work_name)
                                    else:
                                        use_google_form.alarm_recover(domain, domain_local_time, "", machine, event_id, update_google_sheet_title, share_link_temp[0], work_name)

                                #恢復    
                                else:
                                    if len(update_google_sheet_title) >=18:
                                        use_google_form.alarm_recover(domain, domain_local_time, domain_local_time, machine, event_id, '多地區', share_link_temp[0], work_name)          
                                    else:
                                        use_google_form.alarm_recover(domain, domain_local_time, domain_local_time, machine, event_id, update_google_sheet_title, share_link_temp[0], work_name)          


                       

                    except:
                        #成功取出最後一個domain 進行檢測 不成功就從except塞回去
                        csv_data.append(detection_data)
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
                    csv_data.append(detection_data)
                    #計算目前 domain 檢測進度
                    count -= 1
                    break
                
                # finally:
                #     for i in temp_repeat_domain_result:
                #         finally_title_domain_result.append(i)



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

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



#建立Excel
# wb = openpyxl.Workbook()    # 建立空白的 Excel 活頁簿物件
# s1 = wb.active

# title = ['域名', '探測點', 'IP', '狀態', '分享連結']
# s1.append(title)


# # 彙整到Excel
# for k in finally_title_domain_result:
#         s1.append(k)
# wb.save(f'{wb_name}.xlsx')


#程式結束執行時間
program_end_localtime = time.localtime()
program_end_localtime_result = time.strftime("%Y-%m-%d %I:%M:%S %p", program_end_localtime)
program_end_time = time.time()

program_run_time = round(program_end_time - program_start_time)
hour = program_run_time // 3600
minute = (program_run_time - 3600 * hour) // 60
second = program_run_time - 3600 * hour - 60 * minute

print(f'域名已全數檢測完畢!\n開始時間: {program_start_localtime_result}\n結束時間: {program_end_localtime_result}\n總計時間: {hour}:{minute}:{second}')




