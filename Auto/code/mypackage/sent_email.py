from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#SMTP server
import smtplib

import requests as rq
from bs4 import BeautifulSoup as bs
import socket
import random
from datetime import datetime

import mypackage.gmail_information as gmail_information

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

#First crawler IP
def first_ip():
    response = rq.get('https://api.ipify.org?format=json', headers=HEADER)
    data = response.json()
    ip = data['ip'] 
    return ip

# Second crawler IP
def second_ip():
    response = rq.get('https://www.ez2o.com/App/Net/IP', headers=HEADER)
    soup = bs(response.text, "html.parser")
    soup = soup.select_one('strong:-soup-contains("IP位址：")').find_next('td').text.strip()
    ip = soup.split('主機名稱')[0]
    return ip

# Third crawler IP
def third_ip():
    response = rq.get('https://www.whatismyip.com.tw/tw/', headers=HEADER)
    soup = bs(response.text, "html.parser")
    ip = soup.select('b')[0].text
    return ip

# Fourth crawler IP
def fourth_ip():
    response = rq.get('https://myip.com.tw/', headers=HEADER)
    soup = bs(response.text, "html.parser")
    ip = soup.select('font')[0].text
    return ip


random_number = random.randint(1, 4)
if random_number == 1:
    ip = first_ip()
elif random_number == 2:
    ip = second_ip()
elif random_number == 3:
    ip = third_ip()
elif random_number == 4:
    ip = fourth_ip()

external_ip = ip

#message content
content = MIMEMultipart()  #crrate MIMEMultipart object
content["subject"] = "偵測到有人使用您的Code!"  #message title
content["from"] = gmail_information.sender  #sender
content["to"] = gmail_information.recipient #recipient
content['Importance'] = 'high'
content.attach(MIMEText(f"CurrentTime:{currentTime}\nHostname:{hostname}\nLocal IP:{ip_address}\nExternal IP:{external_ip}"))  #email content


#by SMTP Server sent 
with smtplib.SMTP(host='smtp.gmail.com', port="587") as smtp:
    smtp.ehlo()#verify SMTP server
    smtp.starttls() #Create encrypted transmission
    smtp.login(gmail_information.sender, gmail_information.program_password)#login sender Gmail
    smtp.send_message(content)

