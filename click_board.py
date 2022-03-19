#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/10/22 19:44
# @Author : Box
# @File : click_board.py
# @Software: PyCharm

import win32clipboard as w


def setText(text="English testing, 中文测试"):
	# set clipboard data
	w.OpenClipboard()
	w.EmptyClipboard()
	w.SetClipboardText(text)
	w.CloseClipboard()


def getText():
	# get clipboard data
	w.OpenClipboard()
	data = w.GetClipboardData()
	w.CloseClipboard()
	return data


a = getText().split('_')
b = a[0]

setText(text=b)
print(getText())


