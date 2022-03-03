#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import shutil
import time
import datetime
import configparser

config = configparser.ConfigParser()

# 位置信息配置
Temp_path = r'C:\Users\box\Desktop\Nav\Temp'
M_Temp_path = r'D:\M_Temp'
photo_path = r'F:\Photo\截图\自动保存'

Temp_Filename = os.listdir(Temp_path)
M_Temp_Filename = os.listdir(M_Temp_path)
photo_Filename = os.listdir(photo_path)

path_dic = {r'D:\M_Temp': 30,
            r'C:\Users\box\Desktop\Nav\Temp': 7,
            r'F:\Photo\截图\自动保存': 30,
            r'F:\Download\IDM_Download\压缩文件': 60,
            r'F:\Download\IDM_Download\文档': 60,
            r'F:\Download\IDM_Download\程序': 60,
            r'F:\Download\IDM_Download\常规': 60,
            r'F:\Download\chromeDownload': 60,
            r'F:\Download\BaiduNetdiskDownload': 60}
path_name = list(path_dic.keys())


def read_ini(inikey):
    config.read(os.path.join(os.getcwd(), 'path_time.ini'), encoding="utf-8-sig")
    convaluse = config.options(inikey)  # 获取option
    return convaluse

# 写入Del_log文件


def write_log(path, name, ty, con):
    with open(os.path.join(path, 'Del_log.txt'), 'a') as f:
        if ty is 'file':
            f.write(con + '   ' + 'file:  ' + name)
            f.write('\n')
        else:
            f.write(con + '   ' + 'folder:  ' + name)
            f.write('\n')
        f.close


# 判断文件类型
def file_or_folder(path):
    if os.path.isfile(path):
        return 'file'  # 文件
    else:
        return 'folder'  # 文件夹


# 把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12
def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


# 计算两个日期相差天数，自定义函数名，和两个日期的变量名。
def Caltime(date1, date2):
    # %Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。
    date1 = time.strptime(date1, "%Y-%m-%d %H:%M:%S")
    # date2 = time.strptime(date2, "%Y-%m-%d %H:%M:%S")
    # date1 = time.strptime(date1, "%Y-%m-%d")
    # date2 = time.strptime(date2, "%Y-%m-%d")
    # 根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推...
    # date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
    # date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    # date2 = datetime.datetime(date2[0], date2[1], date2[2])
    # 返回两个变量相差的值，就是相差天数
    return (date2 - date1).days


# 获取文件的修改时间
def get_FileModifyTime(filepath):
    t = os.path.getmtime(filepath)
    return TimeStampToTime(t)  # type str


# 删除文件
def file_del(path, name, t):
    file = os.path.join(path, name)
    M_time = get_FileModifyTime(file)
    N_time = datetime.datetime.now()
    if Caltime(M_time, N_time) > t and name != 'desktop.ini':
        if file_or_folder(file) is 'file':
            try:
                os.remove(file)
                write_log(path, name, 'file', '√')
            except BaseException:
                write_log(path, name, 'file', '×')

        else:
            try:
                # os.system("rd /q /s %s" % file)
                shutil.rmtree(file)
                write_log(path, name, 'folder', '√')
            except BaseException:
                write_log(path, name, 'folder', '×')


def log_init(path):
    file = os.path.join(path, 'Del_log.txt')
    # folder = os.path.join(path, 'Del_log')
    # os.mkdir(folder)
    if os.path.exists(file):
        os.remove(file)
    fd = open(file, mode="w", encoding="utf-8")
    fd.write('        ******************************\n')
    fd.write('        *****      ' + str(time.strftime("%Y-%m-%d")) + '     *****\n')
    fd.write('        ******************************\n')
    fd.close()


def deal(path, name, t):
    log_init(path)
    for i in name:
        file_del(path, i, t)


def main():
    # ver1.0 单独处理每个文件夹
    # deal(Temp_path, Temp_Filename, 7)
    # deal(M_Temp_path, M_Temp_Filename, 30)
    # deal(photo_path, photo_Filename, 30)

    # ver2.0 将所有路径和时间整合为列表相互对应
    for i in path_name:
        # file_name = os.listdir(i)
        # deal(path=i, name=file_name, t=path_dic[i])
        print(path_dic[i])

    # ver3.0 将路径和时间信息读取到ini文件，便于修改
    # ini_file = os.path.join(os.getcwd(), 'path_time.ini')
    # if not(os.path.exists(ini_file)):
    #     print('配置文件path_time.ini未找到，请检查文件是否存在')
    #     os.system("pause")
    # p = read_ini("path")
    # t = read_ini("time")
    # for i, j in zip(p, t):
    #     current_path = config.get("path", i)
    #     current_time = config.getint("time", j)
    #     file_name = os.listdir(current_path)
    #     deal(path=current_path, name=file_name, t=current_time)


if __name__ == '__main__':
    main()
