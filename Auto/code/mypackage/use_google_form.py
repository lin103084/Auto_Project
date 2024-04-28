import requests as rq

#輸出來源
#googlesheet URL : https://docs.google.com/spreadsheets/d/1npBQoOFAAROKB1RbxnJzIWx-_ySNc/edit?usp=sharing
def google_form(domain, all_ban, status_count_all, status_count_not610, status_count_610, share_linkm, work_name):

    url = 'https://docs.google.com/forms/u/1/d/e/1FAIpQLSfZHbje4muzLOrXLXVojQ3t94sq5cK69_UA1mzsa3Q/formResponse'
    parmas = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36'
    }


    data = {
        #域名
        'entry.111043525': domain,

        #異常地區 - 全部
        'entry.1083300954': all_ban,

        #全部異常 - 筆數
        'entry.1949147648': status_count_all,

        #非超時異常 - 筆數
        'entry.331623291': status_count_not610,

        #超時異常  - 筆數1
        'entry.313703961': status_count_610,

        #link
        'entry.1515258988': share_linkm,

        #work_name
        'entry.608931814': work_name

    }

    res = rq.post(url, params=parmas, data=data)
    print(f'{domain} / Google_sheet 提交成功!')


#   VS域名查詢紀錄 Ver 2.1
#   googlesheet URL : https://docs.google.com/forms/d/e/1FAIpQLSfzvhDoykRQdjPJEHaATRmafuHuopYyM3O6T3df-nQ/viewform
def alarm_recover(domain, domain_local_time, domain_recover_time, machine, event_id, all_ban, share_link , work_name):
    url = 'https://docs.google.com/forms/u/0/d/e/1FAIpQLSfzvhDoykRQdjPJZuk3mRmafuHuopYyM3O6T3df-nQ/formResponse'
    parmas = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36'
    }

    data = {
        #域名
        'entry.55020332': domain,

        #探點機
        'entry.714164759': machine,

        #事件ID
        'entry.776537112': event_id,

        #發生時間
        'entry.711037768': domain_local_time,

        #恢復時間
        'entry.2098429519': domain_recover_time,
        
        #分享連結
        'entry.271431809': share_link,

        #操作人員
        'entry.130949564': work_name,

        #封禁地區
        # 'entry.748818286': all_ban,

        #汙染地區
        'entry.1553178369': all_ban,

    }
    res = rq.post(url, params=parmas, data=data)
    print(f'{domain} / Google_sheet 提交成功!\n分享連結:{share_link}')

