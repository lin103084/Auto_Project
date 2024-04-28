import telegram
import asyncio

import requests as rq
from bs4 import BeautifulSoup as bs
import socket
import random
from datetime import datetime

import mypackage.telegrame_information as telegrame_information


#Current Time
currentDateAndTime = datetime.now()
currentTime = currentDateAndTime.strftime("%Y-%m-%d %p %I:%M:%S ")

# Get local hostname
hostname = socket.gethostname()
# Get local ip
ip_address = socket.gethostbyname(hostname)

# Get local external ip
HEADER = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36'
}

#crawler IP
def ip_1():
    try:
        response = rq.get('https://api.ipify.org?format=json', headers=HEADER)
        data = response.json()
        ip = data['ip'] 
        return ip
    except:
        return "Failed to obtain external IP"

#crawler IP
def ip_2():
    try:
        response = rq.get('https://www.ez2o.com/App/Net/IP', headers=HEADER)
        soup = bs(response.text, "html.parser")
        soup = soup.select_one('strong:-soup-contains("IP位址：")').find_next('td').text.strip()
        ip = soup.split('主機名稱')[0]
        return ip
    except:
        return "Failed to obtain external IP"

#crawler IP
def ip_3():
    try:
        response = rq.get('https://www.whatismyip.com.tw/tw/', headers=HEADER)
        soup = bs(response.text, "html.parser")
        ip = soup.select('b')[0].text
        return ip
    except:
        return "Failed to obtain external IP"
    
#crawler IP
def ip_4():
    try:
        response = rq.get('https://myip.com.tw/', headers=HEADER)
        soup = bs(response.text, "html.parser")
        ip = soup.select('font')[0].text
        return ip
    except:
        return "Failed to obtain external IP"
    
    
#crawler IP
def ip_5():
    try:
        response = rq.get('https://tool.magiclen.org/ip/', headers=HEADER)
        ip = response.text        
        return ip
    except:
        return "Failed to obtain external IP"

#crawler IP
def ip_6():
    try:
        response = rq.get('https://tool.lu/ip/', headers=HEADER)
        soup = bs(response.text, "html.parser")
        soup = soup.find(id="main_form").select_one('p').text
        ip = soup.split('你的外网IP地址是：')[1]
        return ip
    except:
        return "Failed to obtain external IP"    

#crawler IP
def ip_7():
    try:
        response = rq.get('https://youtils.cc/geoip', headers=HEADER)
        soup = bs(response.text, "html.parser")
        ip = soup.find('input', {'ref': 'defaultHost', 'type': 'hidden'})['value']
        return ip
    except:
        return "Failed to obtain external IP"    

#crawler IP   
def ip_8():
    try:
        response = rq.get('https://www.whois365.com/tw/', headers=HEADER)
        soup = bs(response.text, "html.parser")
        ip = soup.find("p", class_='ip').find('span').find('a').text
        return ip
    except:
        return "Failed to obtain external IP"  
    




#random crawler external ip
random_number = random.randint(1, 8)
if random_number == 1:
    ip = ip_1()
elif random_number == 2:
    ip = ip_2()
elif random_number == 3:
    ip = ip_3()
elif random_number == 4:
    ip = ip_4()
elif random_number == 5:
    ip = ip_5()
elif random_number == 6:
    ip = ip_6()
elif random_number == 7:
    ip = ip_7()
elif random_number == 8:
    ip = ip_8()

#external IP
external_ip = ip



#sent message to bot
async def send_message():
    # API Token
    bot_token = telegrame_information.bot_token
    # Create bot 
    bot = telegram.Bot(token=bot_token)

    # Group chat id
    chat_id = telegrame_information.chat_id  

    # sent message to group
    message_text = f'偵測到有人正在使用您的Code!\n\nCurrentTime:{currentTime}\nHostname:{hostname}\nLocal IP:{ip_address}\nExternal IP:{external_ip}'
    await bot.send_message(chat_id=chat_id, text=message_text)

# if __name__ == "__main__":
#     asyncio.run(send_message())
asyncio.run(send_message())