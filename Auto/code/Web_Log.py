import time
import openpyxl
import os

from datetime import datetime, timedelta, timezone
from mypackage import use_web_log
from mypackage import sent_telegram_bot
from mypackage import login_password


LOGINPASSWORD = login_password.PASSWORD
while True:
    answer = input("請輸入密碼:")
    if answer == LOGINPASSWORD:
        break
    print("輸入錯誤")



# 1 = Info 2 = Error
INDEX = {1 : "bec52020-9f1a-11ee-a511-ada40c7ae21f", 2 : "d1b9e0d0-9f1a-11ee-a511-ada40c7ae21f"}

SERVICE = {
            1: "app1-service",
            2: "app2-service",
            3: "app3-service",
            4: "app4-service",
            5: "app5-service",
            6: "app6-service",
            7: "app7-service",
            8: "app8-service",
            9: "app9-service",
            10: "app10-service",
            11: "app11-service",
            12: "app12-service",
            13: "app13-service",
            14: "app14-service",
            15: "app15-service",
            16: "app16-service",
            17: "app17-service",
            18: "app18-service",
            19: "app19-service",
            20: "app20-service",
            21: "app21-service",
            22: "app22-service",
            23: "app23-service",
            24: "app24-service",
            25: "app25-service",
            26: "app26-service",
            27: "app27-service",
            28: "app28-service",
            29: "app29-service",
            30: "app30-service",
            31: "app31-service",
            32: "app32-service",
            33: "app33-service",
            34: "app34-service",
            35: "app35-service",
            36: "app36-service",
            37: "app37-service",
            38: "app38-service",}

HOSTNAME = ["aws-b-app01", "aws-b-app02", "aws-b-app03", "aws-b-app04", "aws-b-app05", "aws-b-app06", "aws-b-app07", "aws-b-app08"]

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def dateTime(DATE, TIME):
# 合併日期和時間，並轉換為datetime對象
    manual_input_time_str = f'{DATE} {TIME[:2]}:{TIME[2:4]}:{TIME[4:]}'
    manual_input_time = datetime.strptime(manual_input_time_str, '%Y-%m-%d %H:%M:%S')
    # 獲取UTC時區
    utc_timezone = timezone.utc
    # 將手動輸入的時間轉換為UTC
    manual_input_time_utc = manual_input_time.replace(tzinfo=utc_timezone)
    # 進行時間調整
    adjusted_time_utc = manual_input_time_utc - timedelta(hours=8)
    # 將調整後的時間格式化為字符串，修改格式化字符串
    adjusted_time_str = adjusted_time_utc.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    return adjusted_time_str




#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
if __name__ == "__main__":
    # 輸入開始日期時間
    start_date = input("請輸入開始日期（格式：YYYY-MM-DD）：")
    start_time = input("請輸入開始時間（格式：HHMMSS）：")
    # 輸入結束日期結束
    end_date = input("請輸入結束日期（格式：YYYY-MM-DD）：")
    end_time = input("請輸入結束時間（格式：HHMMSS）：")
    start_datetime = dateTime(start_date, start_time)
    end_datetime = dateTime(end_date, end_time)


    # 輸入INFO　ERROR
    while True:
        index = int(input("請輸要查詢 1.INFO 2.ERROR：\n"))
        if index in INDEX and index == 1:
            INDEX_STATUS = 'Info'
            break
        elif index in INDEX and index == 2:
            INDEX_STATUS = 'Error'
            break
    index = INDEX[index]

    
    # 輸入查詢的服務
    while True:            
        service = int(input(
                        '請輸入要查詢的服務:\n' 
                        "1.app1-service\n"
                        "2.app2-service\n"
                        "3.app3-service\n"
                        "4.app4-service\n"
                        "5.app5-service\n"
                        "6.app6-service\n"
                        "7.app7-service\n"
                        "8.app8-service\n"
                        "9.app9-service\n"
                        "10.app10-service\n"
                        "11.app11-service\n"
                        "12.app12-service\n"
                        "13.app13-service\n"
                        "14.app14-service\n"
                        "15.app15-service\n"
                        "16.app16-service\n"
                        "17.app17-service\n"
                        "18.app18-service\n"
                        "19.app19-service\n"
                        "20.app20-service\n"
                        "21.app21-service\n"
                        "22.app22-service\n"
                        "23.app23-service\n"
                        "24.app24-service\n"
                        "25.app25-service\n"
                        "26.app26-service\n"
                        "27.app27-service\n"
                        "28.app28-service\n"
                        "29.app29-service\n"
                        "30.app30-service\n"
                        "31.app31-service\n"
                        "32.app32-service\n"
                        "33.app33-service\n"
                        "34.app34-service\n"
                        "35.app35-service\n"
                        "36.app36-service\n"
                        "37.app37-service\n"
                        "38.app38-service\n"
                        ))
        if service in SERVICE:
            break


    service = SERVICE[service]
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    result_short_url = []
    for host in HOSTNAME:
        URL = f"https://weblog.zbxop.online/app/discover#/?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:'{start_datetime}',to:'{end_datetime}'))&_a=(columns:!(service,hostname,message),filters:!(),index:{index},interval:auto,query:(language:kuery,query:'service%20:%22{service}%22%20and%20hostname%20:%22{host}%22%20'),sort:!(!('@timestamp',desc)))"
        
        short_url = use_web_log.short_url(start_datetime, end_datetime, index, service, host)
        # print(URL)
        print(short_url)
        # time.sleep(3)
        result_short_url.append([service, host, short_url])
        time.sleep(0.5)

    

    path = '../' 
    os.chdir(path=path)
    os.chdir(path=path)

    #Save to Excel
    workbook = openpyxl.Workbook()
    sheet1 = workbook.active

    title = ['Service','HostName', 'ShortURL']
    sheet1.append(title)

    #save to excel
    for i in result_short_url:
        sheet1.append(i)
    
    workbook.save(f'{service}_{INDEX_STATUS}_{start_date}-{start_time}_{end_date}-{end_time}.xlsx')

    print('輸出完成!')



        
