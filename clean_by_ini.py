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
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S',
                    filename='my.log',
                    filemode='w')

try:
    import send2trash
    from win10toast import ToastNotifier


    logging.info('获取扩展库成功！开始执行主程序。')
except Exception as e:
    logging.error('获取扩展库失败，退出执行！请检查环境配置是否正常！！')
    exit(-1)

toaster = ToastNotifier()


def read_ini(inikey):
    try:
        path = os.path.join(os.getcwd(), 'path_time.ini')
        config.read(path, encoding="utf-8")
        logging.debug(path)
        convaluse = config.options(inikey)  # 获取option
        return convaluse
    except BaseException:
        logging.error('没有找到配置文件!!')
        toaster.show_toast("Run Cleaner",
                           "没有找到配置文件",
                           icon_path=None,
                           duration=5)
        while toaster.notification_active():
            time.sleep(0.1)
        raise RuntimeError('没有配置文件')


def Caltime1(date1, date2):
    date1 = time.strptime(date1, "%Y-%m-%d")
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    return (date2 - date1).days


# 计算两个日期相差天数，自定义函数名，和两个日期的变量名。
def Caltime(date1, date2):
    # %Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。
    date1 = time.strptime(date1, "%Y-%m-%d %H:%M:%S")
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    return (date2 - date1).days


# 获取文件的修改时间
def get_FileModifyTime(filepath):
    t = os.path.getmtime(filepath)
    return TimeStampToTime(t)  # type str


def file_or_folder(path):
    if os.path.isfile(path):
        return 'file'  # 文件
    else:
        return 'folder'  # 文件夹


# 把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12
def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


def get_old_data(path):
    file = os.path.join(path, 'Del_log.txt')
    old_data_ = []
    try:
        fr = open(file, mode="r+", encoding='gbk')
        for i in fr:
            tt = re.findall('[0-9]{4}-[0-9]{2}-[0-9]{2}', i)
            # print(tt)
            if tt != [] and Caltime1(tt[0], datetime.datetime.now()) > 30:
                # print(tt)
                break
            old_data_.append(i)
        fr.close()
    except FileNotFoundError:
        logging.error("File is not found. Recreat the log file.")
        print("File is not found. Recreat the log file.")
        fr = open(file, mode="a+", encoding='gbk').close()
    except PermissionError:
        logging.error("File is not found. Recreat the log file.")
        print("You don't have permission to access this file.")
    return old_data_


def get_data_del(path, t):
    now_data_ = []
    file_name = os.listdir(path)
    n_time = datetime.datetime.now()
    for name in file_name:
        file = os.path.join(path, name)
        m_time = get_FileModifyTime(file)
        if Caltime(m_time, n_time) > int(t) and name != 'desktop.ini' and name != 'Del_log.txt':
            if file_or_folder(file) == 'file':
                try:
                    # os.remove(file)
                    send2trash.send2trash(file)
                    now_data_.append('√' + '   ' + 'file:  ' + name + '\n')
                except BaseException:
                    now_data_.append('×' + '   ' + 'file:  ' + name + '\n')

            else:
                try:
                    # os.system("rd /q /s %s" % file)
                    # shutil.rmtree(file)
                    send2trash.send2trash(file)
                    now_data_.append('√' + '   ' + 'folder:  ' + name + '\n')
                except BaseException:
                    now_data_.append('×' + '   ' + 'folder:  ' + name + '\n')
    return now_data_


def write_log(path, now_data_, old_data_):
    with open(os.path.join(path, 'Del_log.txt'), 'w+') as f:
        f.seek(0)
        f.write('      *****      ' + str(time.strftime("%Y-%m-%d")) + '     *****\n')
        for i in now_data_:
            f.write(i)
        for j in old_data_:
            f.write(j)
        f.close


def run_clean():
    p = read_ini("path")
    t = read_ini("time")
    for i, j in zip(p, t):
        now_path = config.get("path", i)
        now_time = config.get("time", j)
        if not os.path.exists(now_path):
            logging.error("path is not exist: " + now_path)
            continue
        old_data = get_old_data(now_path)
        now_data = get_data_del(now_path, now_time)
        write_log(now_path, now_data, old_data)


def main():
    toaster.show_toast("Run Cleaner",
                       "开始清理!",
                       icon_path=None,
                       duration=5,
                       threaded=True)
    run_clean()
    time.sleep(7)
    toaster.show_toast("清理完成！",
                       "ok",
                       icon_path=None,
                       duration=5,
                       threaded=True)

    # 等待线程通知完成
    while toaster.notification_active():
        time.sleep(0.1)


if __name__ == '__main__':
    main()
