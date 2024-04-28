import requests as rq
def short_url(start_datetime, end_datetime, index, service, host):
    try:
        url = 'https://weblog.zbxop.online/api/shorten_url'
        headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-TW,zh;q=0.9",
            "Connection":"keep-alive",
            "Content-Length":"405",
            "Content-Type":"application/json",
            "Host":"weblog.zbxop.online",
            "Kbn-Version":"7.14.2",
            "Origin":"https://weblog.zbxop.online",
            "Referer":"https://weblog.zbxop.online/app/discover",
            "Sec-Ch-Ua":'"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            "Sec-Ch-Ua-Mobile":"?0",
            "Sec-Ch-Ua-Platform":"Windows",
            "Sec-Fetch-Dest":"empty",
            "Sec-Fetch-Mode":"cors",
            "Sec-Fetch-Site":"same-origin",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        }

        data = {"url":
                f"/app/discover#/?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:'{start_datetime}',to:'{end_datetime}'))&_a=(columns:!(service,hostname,message),filters:!(),index:{index},interval:auto,query:(language:kuery,query:'service%20:%22{service}%22%20and%20hostname%20:%22{host}%22%20'),sort:!(!('@timestamp',desc)))"}
        
        response = rq.post(url=url, headers=headers, json=data).json()

        return "https://weblog.zbxop.online/goto/" + response["urlId"]
    
    except:
        return "請求失敗!"