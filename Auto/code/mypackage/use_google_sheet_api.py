import pygsheets
import pandas as pd
import os

def google_sheet(data):
# mst 
    temp_path = os.getcwd() + '\google_sheet_api_token\mst-project-32917-c6ba38b9747b.json'  
    print('temp_path:')
    print(temp_path)

    path = temp_path
    print('path:')
    print(path)
    
                                                                      
    gc = pygsheets.authorize(service_file= path)

    sht = gc.open_by_url(
    'https://docs.google.com/spreadsheets/d/1npBQ9dMjhi9oOFAARER8TPtdfhk7RbxnJzIWx-_ySNc/edit#gid=2074887317'
    )

  
    #選取sheet by名稱
    wks = sht.worksheet_by_title("資料統計")

    #讀取舊google sheet資料
    old_df = wks.get_as_df().iloc[:, 0:5]



    #要加判斷的原因是，如果原來的google sheet 內沒有資料，會從第三個row 開始新增資料
    #所以才使用此方式去判斷
    #使用第一筆資料的 域名 長度 去做判斷條件
    if len(old_df.values[0][0]) >= 5:
        #新資料
        new_data = data

        #新資料轉成dataframe
        new_df = pd.DataFrame(new_data, columns=('域名', '探測點', 'IP', '狀態', '分享連結'))

        #新舊資料合併
        df_all = pd.concat([old_df, new_df], axis=0)

        #更新到google sheet
        wks.set_dataframe(df_all, 'A1') #從欄位 A1 開始

    else:
        new_data = data
        #新資料轉成dataframe
        new_df = pd.DataFrame(new_data, columns=('域名', '探測點', 'IP', '狀態', '分享連結'))
        #更新到google sheet
        wks.set_dataframe(new_df, 'A1') #從欄位 A1 開始

