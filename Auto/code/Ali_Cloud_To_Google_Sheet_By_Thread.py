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
import random

#write package by me
from mypackage import use_wait_method as wait
from mypackage import use_readfile
from mypackage import use_google_form
from mypackage import use_google_sheet_api
from mypackage import use_selenium_anti_reptitle
from mypackage import sent_telegram_bot
from mypackage import login_password

LOGINPASSWORD = login_password.PASSWORD
while True:
    answer = input("請輸入密碼:")
    if answer == LOGINPASSWORD:
        break
    print("輸入錯誤")
#Path to the original
original_path = os.getcwd()

#Path change
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
#worker
work_name_dic = {
    "1" : "Byron",
    "2" : "Wilson",
    "3" : "Fisher",
    "4" : "Armin",
    "5" : "Dave",
    "6" : "Jason",
    "7" : "Tommy",
    "8" : "Jane"
}

while True:
    work_name_temp = input('\n請選擇操作夥伴\n1.Byron   2.Wilson   3.Fisher   4.Armin   5.Dave   6.Jason   7.Tommy   8.Jane\n當前操作夥伴 : ')

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
print()
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# 導入Dns資料
domain_excel = use_readfile.excel_file()

# 計算Domain總數量
domain_excel_len = len(domain_excel)

#Domain檢測計次
count = 0

#判斷是否為主要的封禁Dns結果 
finally_title_domain_result = []
''''''''''''''''''''''''''''''''''''''''''''''''''''''
#程式開始執行時間
program_start_localtime = time.localtime()
program_start_localtime_result = time.strftime("%Y-%m-%d %I:%M:%S %p", program_start_localtime)
program_start_time = time.time()

start_wb_name_localtime = time.localtime()  
start_wb_name_localtime = time.strftime("%Y%m%d_%H_%M_%S", start_wb_name_localtime)


def crawler():
    global count
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


                            #整理並提交到google sheet
                            if temp_count == 0:
                                temp_repeat_domain_result.append([domain, "", "", "", share_link_temp[0]])    
                                use_google_form.google_form(domain, "", 0, 0, 0, share_link_temp[0], work_name)

                            else:
                                # update_google_sheet_domain = set() #domain
                                # update_google_sheet_share_link = set() #share_link

                                update_google_sheet_title = [] #全部封禁地區

                                update_google_sheet_all_status = [] #全部狀態
                                update_google_sheet_not610_status = [] #非610狀態
                                update_google_sheet_610_status = [] #610狀態

                                #[domain, 地區, IP, 狀態, share_link]
                                for k in temp_repeat_domain_result:
                                    # update_google_sheet_domain.add(k[0])
                                    # update_google_sheet_share_link.add(k[-1])
                        
                                    update_google_sheet_title.append(k[1])

                                    update_google_sheet_all_status.append(k[3])
                                    if k[3] != '610':
                                        update_google_sheet_not610_status.append(k[3])
                                    else:
                                        update_google_sheet_610_status.append(k[3])
                                
                                #提交到google sheet
                                #將集合 轉回list 才有辦法 篩選
                                # update_google_sheet_domain = list(update_google_sheet_domain)
                                # update_google_sheet_share_link = list(update_google_sheet_share_link)

                                use_google_form.google_form(
                                    domain, #域名
                                    update_google_sheet_title, #全部封禁地區
                                    len(update_google_sheet_all_status),#全部狀態
                                    len(update_google_sheet_not610_status),#非610狀態
                                    len(update_google_sheet_610_status),#610狀態
                                    share_link_temp[0], #share_link
                                    work_name #執行人員
                                )                 

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

                            #整理並提交到google sheet
                            if temp_count == 0:
                                temp_repeat_domain_result.append([domain, "", "", "", share_link_temp[0]])    
                                use_google_form.google_form(domain, "", 0, 0, 0, share_link_temp[0], work_name)

                            else:
                                # update_google_sheet_domain = set() #domain
                                # update_google_sheet_share_link = set() #share_link

                                update_google_sheet_title = [] #全部封禁地區

                                update_google_sheet_all_status = [] #全部狀態
                                update_google_sheet_not610_status = [] #非610狀態
                                update_google_sheet_610_status = [] #610狀態

                                #[domain, 地區, IP, 狀態, share_link]
                                for k in temp_repeat_domain_result:
                                    # update_google_sheet_domain.add(k[0])
                                    # update_google_sheet_share_link.add(k[-1])
                        
                                    update_google_sheet_title.append(k[1])

                                    update_google_sheet_all_status.append(k[3])
                                    if k[3] != '610':
                                        update_google_sheet_not610_status.append(k[3])
                                    else:
                                        update_google_sheet_610_status.append(k[3])
                                
                                #提交到google sheet
                                #將集合 轉回list 才有辦法 篩選
                                # update_google_sheet_domain = list(update_google_sheet_domain)
                                # update_google_sheet_share_link = list(update_google_sheet_share_link)

                                use_google_form.google_form(
                                    domain, #域名
                                    update_google_sheet_title, #全部封禁地區
                                    len(update_google_sheet_all_status),#全部狀態
                                    len(update_google_sheet_not610_status),#非610狀態
                                    len(update_google_sheet_610_status),#610狀態
                                    share_link_temp[0], #share_link
                                    work_name #執行人員
                                )                 

                       

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

''''''''''''''''''''''''''''''''''''''''''''''''''''''

# 彙整到Excel
wb = openpyxl.Workbook()    
s1 = wb.active

title = ['域名', '探測點', 'IP', '狀態', '分享連結']
s1.append(title)

for k in finally_title_domain_result:
        s1.append(k)

#創建隨機數，讓檔案生成時不會重複
random_int = str(round(random.randint(0, 10000), 3))
wb.save(start_wb_name_localtime + '__' + end_wb_name_localtime + '__' + random_int + '.xlsx')
print(f'域名已全數檢測完畢!\n開始時間: {program_start_localtime_result}\n結束時間: {program_end_localtime_result}\n總計時間: {hour}:{minute}:{second}')


#提交Google sheet資料
check_list = ['1']
while True:
    check = input('\n資料上傳至Google Sheet 資料統計\n請輸入 1 : ')
    if check in check_list: 
        os.chdir(original_path)
        use_google_sheet_api.google_sheet(finally_title_domain_result)
        break

    else:
        print("\n請輸入以上對應的阿拉伯數字!!!")


print('Google Sheet資料已上傳!')





