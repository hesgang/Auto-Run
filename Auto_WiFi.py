#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import sys

import pywifi, time, os
from pywifi import const
from config import *


def get_wifi_key(_name):
    return config.get('wifi', _name)


def is_connected(wifi_inter):
    if wifi_inter.status() in [const.IFACE_CONNECTED, const.IFACE_INACTIVE]:
        return True
    else:
        return False


def connet_wifi(wifi_inter, wifi_profile):
    # wifi_inter.remove_all_network_profiles()  # 删除其它配置文件
    tmp_profile = wifi_inter.add_network_profile(wifi_profile)  # 加载配置文件
    wifi_inter.connect(tmp_profile)
    time.sleep(2)
    if wifi_inter.status() == const.IFACE_CONNECTED:
        return True
    else:
        return False


def set_profile(wifi_name):
    wifi_profile = pywifi.Profile()  # 配置文件
    wifi_profile.ssid = wifi_name  # wifi名称
    wifi_profile.auth = const.AUTH_ALG_OPEN  # 需要密码
    wifi_profile.akm.append(const.AKM_TYPE_WPA2PSK)  # 加密类型
    wifi_profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元
    wifi_profile.key = get_wifi_key(wifi_name)  # wifi密码
    return wifi_profile


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
            print('该WiFi网络故障，尝试更换WiFi')
            iface.disconnect()
            time.sleep(10)
            exit_code = os.system('ping www.baidu.com >D:log.log')
            if exit_code == 0:
                return True
            else:
                return False
        else:
            for profile in wifi_profiles:
                print('尝试连接:{}'.format(profile.ssid))
                iface.connect(profile)
                time.sleep(5)
                if is_internet():
                    break
    else:
        return True


if __name__ == '__main__':
    n = 0
    while True:
        n += 1
        if is_internet() and n > 3:
            break
        time.sleep(1)



    # for i in pro:
    #     print(i.ssid)
    # if not is_connected(iface):
    #     print('网络已断开，重新连接中……')
    #     for name in wifi_names:
    #         n = 0
    #         profile = set_profile(name)
    #         while True:
    #             con = connet_wifi(iface, profile)
    #             n += 1
    #             if not con and n <= 3:
    #                 time.sleep(2)
    #                 continue
    #             else:
    #                 res = '成功' if con else '失败'
    #                 print(f'尝试连接{n}次，连接{res}!')
    #                 break



