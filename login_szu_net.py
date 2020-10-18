# author: zephyr ji
# time: 2020/10/01
# pip install selenium
# download chromedriver：http://chromedriver.storage.googleapis.com/index.html

import time
from selenium import webdriver
import requests
import re

def login(username, password):
    url = 'https://drcom.szu.edu.cn/a70.htm'  # url中指明定位到校园网登陆界面
    chrome_driver = r'F:\software\Anaconda\envs\carla\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe'

    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get(url)
    print(driver.title)
    name_input = driver.find_element_by_id('VipDefaultAccount')  # 找到用户名的框框
    pass_input = driver.find_element_by_id('VipDefaultPassword')  # 找到输入密码的框框
    login_button = driver.find_element_by_xpath('/html/body/div/div/div[2]/form[2]/div[2]/input[1]')  # 找到登录按钮
    # reset_button = driver.find_element_by_id('VipResetButton')  # 找到reset按钮

    name_input.clear()
    name_input.send_keys(username)  # 填写用户名
    time.sleep(0.2)
    pass_input.clear()
    pass_input.send_keys(password)  # 填写密码
    time.sleep(0.2)
    login_button.click()  # 点击登录

    time.sleep(10)
    print(driver.title)

    driver.close()

def canConnect():
    try:
        q = requests.get("http://www.baidu.com", timeout=5)
        m = re.search(r'STATUS OK', q.text)
        if m:
            return True
        else:
            return False
    except:
        print('error')
        return False


if __name__ == "__main__":
    user = "322167"  # 输入账号
    pw = "jzf1230."  # 输入密码
    while True:
        can_connect = canConnect()
        getCurrentTime = time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
        if not can_connect:
            print(getCurrentTime, u"断网了...")
            login(user, pw)
            print(getCurrentTime, u"诶，我又好了...")
            time.sleep(10)
        else:
            print(getCurrentTime, u"一切正常...")
            time.sleep(60)