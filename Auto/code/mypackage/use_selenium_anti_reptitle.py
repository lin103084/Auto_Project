from selenium.webdriver.chrome.options import Options
import random

UA = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0) Gecko/20100101 Firefox/65.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) CriOS/31.0.1650.18 Mobile/11B554a Safari/8536.25",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4",
    "Mozilla/5.0 (Linux; Android 4.2.1; M040 Build/JOP40D) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; M351 Build/KTU84P) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",]

def chrome_options_fun(headless):
    chrome_options = Options()
    if headless == 1: chrome_options.add_argument('--headless')                                     # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    chrome_options.add_argument(f'user-agent={UA[random.randint(0, len(UA)-1)]}')                   # USER-AGENT
    chrome_options.add_argument("--window-size=1920x3000")                                          # 更改畫面大小
    chrome_options.add_argument('blink-settings=imagesEnabled=false')                               # 不加載圖片
    chrome_options.add_argument('--disable-javascript')                                             # 禁用javascript
    #chrome_options.add_argument("--disable-gpu")                                                   # 禁用gpu
    #chrome_options.add_argument('--incognito')                                                     # 无痕模式
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')                    # 眨眼功能=自動化控制
    chrome_options.add_argument('--disable-extensions')                                             # 停用擴充
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-web-security')                                            # 網路安全
    chrome_options.add_argument('--ignore-certificate-errors')                                       # 忽略憑證錯誤
    #chrome_options.add_argument('--no-sandbox')                                                     # 以最高权限运行 部屬Linux要這個參數
    chrome_options.add_argument('--start-maximized')                                                 # 最大化运行（全屏窗口）,不设置，取元素会报错
    #chrome_options.add_argument('--user-data-dir=/dev/null')
    chrome_options.add_argument('--hide-scrollbars')                                                 # 隐藏滚动条, 应对一些特殊页面
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])                 # 設置為開發者模
    chrome_options.add_experimental_option('useAutomationExtension', False)                          # 隐藏正在受到自动软件的控制                                                                                                     
    prefs = { 'profile.default_content_setting_values' :  {'notifications' : 2 }}                    # 禁用浏览器弹窗
    chrome_options.add_experimental_option('prefs',prefs)                                            # 禁用浏览器弹窗

   # 隨機生成或選擇一些權限，以添加到 Chrome 選項中
    random_permissions = ["geolocation", "notifications", "camera", "microphone"]
    selected_permissions = random.sample(random_permissions, k=random.randint(1, len(random_permissions)))

    for permission in selected_permissions:
        chrome_options.add_argument(f'--allow-{permission}')

    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--ignore-gpu-blacklist')



    
    return chrome_options

def chrome_options_fun_2(**kwargs):
    chrome_options = Options()
    
    #Defualt parameter
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--ignore-gpu-blacklist')

    chrome_options.add_argument(f'user-agent={UA[random.randint(0, len(UA)-1)]}')                   # USER-AGENT
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')                    # 眨眼功能=自動化控制
    chrome_options.add_argument("--window-size=1920x3000")                                          # 更改畫面大小
    chrome_options.add_argument("--disable-gpu")                                                    # 禁用gpu
    chrome_options.add_argument('--disable-extensions')                                             # 停用擴充
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-web-security')                                            # 網路安全
    chrome_options.add_argument('--ignore-certificate-errors')                                       # 忽略憑證錯誤
    chrome_options.add_argument('--no-sandbox')                                                      # 以最高权限运行
    
    prefs = { 'profile.default_content_setting_values' :  {'notifications' : 2 }}                    # 禁用浏览器弹窗
    chrome_options.add_experimental_option('prefs',prefs)                                            # 禁用浏览器弹窗
    chrome_options.add_experimental_option('useAutomationExtension', False)                          # 隐藏正在受到自动软件的控制 
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])                 # 設置為開發者模                                                                                        
    
    #Parameter setting
    if kwargs.get("headless", False):chrome_options.add_argument('--headless')                          # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    if kwargs.get("image", False):chrome_options.add_argument('blink-settings=imagesEnabled=false')     # 不加載圖片
    if kwargs.get("javascript", False):chrome_options.add_argument('--disable-javascript')              # 禁用javascript
    if kwargs.get("maximized", False):chrome_options.add_argument('--start-maximized')                  # 最大化运行（全屏窗口）,不设置，取元素会报错
    if kwargs.get("scrollbars", False):chrome_options.add_argument('--hide-scrollbars')                  # 隐藏滚动条, 应对一些特殊页面
    
    # 隨機生成或選擇一些權限，以添加到 Chrome 選項中
    random_permissions = ["geolocation", "notifications", "camera", "microphone"]
    selected_permissions = random.sample(random_permissions, k=random.randint(1, len(random_permissions)))

    for permission in selected_permissions:
        chrome_options.add_argument(f'--allow-{permission}')

    #Bug parmas
    #chrome_options.add_argument('--user-data-dir=/dev/null')
    #chrome_options.add_argument('--incognito')                                                      # 无痕模式
    return chrome_options




'''
https://www.cnblogs.com/testzcy/p/17081401.html

Selenium 隐藏浏览器指纹特征 转载
转载自公众号 AirPython 

大家好，我是安果！

我们使用 Selenium 对网页进行爬虫时，如果不做任何处理直接进行爬取，会导致很多特征是暴露的

对一些做了反爬的网站，做了特征检测，用来阻止一些恶意爬虫

本篇文章将介绍几种常用的隐藏浏览器指纹特征的方式

'''