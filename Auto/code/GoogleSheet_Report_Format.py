import os
import pandas as pd
import pygsheets

from mypackage import report_format_fun
from mypackage import sent_telegram_bot
from mypackage import login_password

LOGINPASSWORD = login_password.PASSWORD
while True:
    answer = input("請輸入密碼:")
    if answer == LOGINPASSWORD:
        break
    print("輸入錯誤")
#Google Sheet 資料導入
gc = pygsheets.authorize(service_account_file='google_sheet_api_token\mst-project-32917-c6ba38b9747b.json')
survey_url = 'https://docs.google.com/spreadsheets/d/16UeTuP79toMu2MdZtDuAZZofklNNwpOhIJNJ0/edit#gid=0'

sh = gc.open_by_url(survey_url)
wks_list = sh.worksheets()
wks = sh[0]


#讀取成 df
df = pd.DataFrame(wks.get_all_records())

#將髒資料做整理，將以下欄位都變成字串
df['告警封禁地區'] = df['告警封禁地區'].astype('str')
df['有恢復封禁地區'] = df['有恢復封禁地區'].astype('str')

#將第一次告警
df['封禁'] = df.apply(report_format_fun.ban_fun, axis = 1)
df['恢復'] = df.apply(report_format_fun.recover_fun, axis = 1)
df.set_index('時間戳記', inplace=True)

#資料篩選
head = int(input('請輸入左側開始列數: '))
tail = int(input('請輸入左側結束列數: '))

#複製一份新的操作 並選需要的欄位
df_copy = df.iloc[head-2:tail,[0, 1, 6, -6, -2, -1]].copy()
#清除所有空值 nan
df_copy = df_copy.replace('nan', "")


#將df資料，用tuple的方式篩選輸出
temp_list = []
for i in df_copy.itertuples():
  temp = []
  temp.append(i.Index)
  temp.append(i.域名)
  temp.append(i.事件ID)
  temp.append(i.告警時間)
  temp.append(i.恢復時間)
  temp.append(i.封禁)
  temp.append(i.恢復)
  temp_list.append(temp)





#分割出 首次封禁 和 恢復封禁
ban = []
resolve = []

for i in temp_list:  
  if i[4] == "":
    ban.append(i)
  else:
    resolve.append(i)

  
     
#根據有恢復封禁，就刪除首次封禁告警
for i in ban:
  for j in resolve:
    if j[-1] =='' and j[-2] =='':
      resolve.pop(resolve.index(j))
    if i[2] == j[2]:
      ban.pop(ban.index(i))


#寫入TXT檔案
tag_name = '@A值班 @B值班'
ban_situation = '您好，以下為域名告警檢測狀況:'
resolve_situation = '您好，以下為域名恢復檢測狀況:'

path = '../' 
os.chdir(path=path)
os.chdir(path=path)

with open('回報格式.txt', 'w', encoding='utf-8') as f:
  #如果沒有資料 就不寫入
    if len(ban) != 0:
        f.writelines(tag_name +'\n')
        f.writelines(ban_situation +'\n')

        for i in ban:
            #如果是多地區 等於已經回報汙染群 就不寫入
            if i[-2] == '多地區' or i[2] == '客服反饋'or i[2] == '主動檢測':
                continue
            #如果沒有封禁地區 就不寫入
            if len(i[-2]) != 0: 
                f.writelines(i[1]+'\n')
                f.writelines('告警時間: ' + i[3] + '\n')
                f.writelines('封禁地區: ' + i[-2] + '\n')

    #寫入空白換行
    f.writelines('\n')
    f.writelines('\n')


  #如果沒有資料 就不寫入
    if len(resolve) != 0:
        f.writelines(resolve_situation +'\n')
        for j in resolve:
            #如果是多地區 等於已經回報汙染群 就不寫入
            if i[-2] == '多地區' or i[2] == '客服反饋'or i[2] == '主動檢測':
                continue

            f.writelines(j[1]+'\n')
            f.writelines('恢復時間: ' + j[4] + "\n")
            f.writelines('告警時間: ' + j[3] + "\n")
            if len(j[-1]) != 0:
                f.writelines('恢復地區: ' + j[-1] + '\n')
            if len(j[-2]) != 0:  
                f.writelines('封禁地區: ' + j[-2] + '\n')

print('輸出完成!')

