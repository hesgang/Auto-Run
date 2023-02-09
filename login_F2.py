#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pywifi, time, os
from pywifi import const

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def is_connected(wifi_inter):
    if wifi_inter.status() in [const.IFACE_CONNECTED, const.IFACE_INACTIVE]:
        return True
    else:
        return False


def re_login():
    my_num = ''
    pwd = ''  # 你的mima

    path = "chromedriver.exe"
    driver = webdriver.Chrome(path)
    # 浏览器最大化
    driver.maximize_window()
    # 访问网站
    url = 'http://172.19.1.2/0.htm'
    driver.get(url=url)
    # 用户名  每个校园网的xpath不同
    user_num = driver.find_element(By.ID, 'username')
    user_num.send_keys(my_num)
    # 密码
    user_password = driver.find_element(By.ID, 'password')
    user_password.send_keys(pwd)
    time.sleep(5)
    # 点击登陆
    user_login = driver.find_element(By.ID, 'submit')
    user_login.click()
    # 关闭
    driver.close()

def is_internet():
    exit_code = os.system('ping www.baidu.com >D:log.log')
    if exit_code != 0:
        wifi = pywifi.PyWiFi()  # 初始化
        iface = wifi.interfaces()[0]  # 选择网卡
        # wifi_names = read_ini('wifi')  # List WiFi名称
        wifi_profiles = iface.network_profiles()
        iface.scan()  # 扫描WiFi
        # wifiresults = iface.scan_results()  # 获取WiFi扫描结果
        if is_connected(iface):
            print('该WiFi网络故障，尝试重新登录')
            re_login()
            time.sleep(5)
            exit_code = os.system('ping www.baidu.com >D:log.log')
            if exit_code == 0:
                print('登录成功')
                return True
            else:
                return False
        else:
            for profile in wifi_profiles:
                if profile.ssid == 'PandoraBox':
                    iface.connect(profile)
                    time.sleep(5)
                else:
                    continue
            if is_internet():
                return True
            else:
                return False
    else:
        return True


if __name__ == '__main__':
    n = 0
    while True:
        n += 1
        if is_internet() and n > 3:
            break
        time.sleep(1)

