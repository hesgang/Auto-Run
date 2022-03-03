#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import shutil
import time
import datetime
import configparser  # 读取配置文件的包
import re

config = configparser.ConfigParser()
logging.basicConfig(level='DEBUG')

def read_ini(inikey):
    config.read(os.path.join(os.getcwd(), 'path_time.ini'), encoding="utf-8")
    convaluse = config.options(inikey)  # 获取option
    return convaluse


# 写入Del_log文件
def write_log(path, name, ty, con):
    with open(os.path.join(path, 'Del_log.txt'), 'a') as f:
        if ty == 'file':
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
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    return (date2 - date1).days


def Caltime1(date1, date2):
    date1 = time.strptime(date1, "%Y-%m-%d")
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
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
    if Caltime(M_time, N_time) > int(t) and name != 'desktop.ini' and name != 'Del_log.txt':
        if file_or_folder(file) == 'file':
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
    fr = open(file, mode="a+", encoding='gbk')
    fr.write('\n        *****      ' + str(time.strftime("%Y-%m-%d")) + '     *****\n')
    fr.seek(0)
    n_text = fr.readlines()
    for i in range(0, len(n_text)):
        tt = re.findall('[0-9]{4}-[0-9]{2}-[0-9]{2}', n_text[i])
        if tt != [] and Caltime1(tt[0], datetime.datetime.now()) < 30:
            te = n_text[i:]
            logging.debug(te)
            break
    fr.close()

    fd = open(file, mode="w")
    fd.writelines(te)
    fd.close()


def deal(path, name, t):
    log_init(path)
    for i in name:
        file_del(path, i, t)


def main():
    p = read_ini("path")
    t = read_ini("time")
    for i, j in zip(p, t):
        now_path = config.get("path", i)
        now_time = config.get("time", j)
        file_name = os.listdir(now_path)
        print(now_time)
        # deal(path=now_path, name=file_name, t=now_time)


if __name__ == '__main__':
    main()
