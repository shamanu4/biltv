# -*- coding: utf-8 -*-

def int_to_4byte(num):
    import struct

    res = []
    binary = struct.pack('!L',num)
    for char in binary:
        res.append(ord(char))

    return res



def short_to_2byte(num):
    import struct

    res = []
    binary = struct.pack('!H',num)
    for char in binary:
        res.append(ord(char))

    return res



def wrap_list(list):
    res = []
    l = len(list)
    for i in range(l):
        res.append(list[l-i-1])

    return res



def int_to_4byte_wrapped(num):
    return wrap_list(int_to_4byte(num))



def short_to_2byte_wrapped(num):
    return wrap_list(short_to_2byte(num))



def byte_and(list1,list2):
    res =[]
    if not len(list1) == len(list2):
        return res
    for i in range(0,len(list1)):
        res.append(list1[i]&list2[i])
    return res


def byte_or(list1,list2):
    res =[]
    if not len(list1) == len(list2):
        return res                                                         
    for i in range(0,len(list1)):
        res.append(list1[i]|list2[i])
    return res


def byte_xor(list1,list2):
    res =[]
    if not len(list1) == len(list2):
        return res                                                         
    for i in range(0,len(list1)):
        res.append(list1[i]^list2[i])
    return res

def latinaze(str):
    return str


def date_formatter(date=None):
    import datetime

    if not date:
        date = datetime.datetime.now()

    day = date.day
    weekday = date.weekday()
    month = date.month
    year = date.year

    thisday = datetime.datetime(year, month, day)
    thisweek = datetime.datetime(year, month, day-weekday)
    thismonth = datetime.datetime(year, month, 1)
    thisyear = datetime.datetime(year, 1, 1)

    return { 'day':thisday, 'week':thisweek, 'month':thismonth, 'year':thisyear }


