#!/usr/bin/env python
# encoding: utf-8

"""
@author: david
@license: Apache Licence 
@contact: davidguy127@gmail.com
@site: 
@software: PyCharm
@file: checkId.py
@time: 8/6/16 10:47 PM
"""

"""
身份证号合法性校验
由身份证号查出出生地，性别
合法性检验考虑了润年，和具体月份对应的天数等情况
由于不太了解是否存在第5，6位全0的身份证号，所以暂且将第5，6位全0的视为合法的地区代码
"""


import time
from json import *


def this_year():
    year = time.strftime('%Y', time.localtime(time.time()))
    return int(year)


def check_year(year):
    y = int(year)
    if len(year) == 2:
        return 0 <= y < 100
    if len(year) == 4:
        return 1900 <= y <= this_year()
    return False


def check_month(month):
    m = int(month)
    return 1 <= m <= 12


def is_leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        return True
    else:
        return False


def check_day(day, month, year):
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    d = int(day)
    m = int(month)
    y = int(year)
    if d > 29 and month == 2:
        return False
    if m == 2:
        if is_leap_year(y):
            return d <= 29
        else:
            return d <= 28
    else:
        return d < days[m-1]


def check_addr(address):
    fp = open('./city_code_json')
    all_addresses = fp.read()
    fp.close()
    addr_dict = JSONDecoder().decode(all_addresses)
    if address in addr_dict:
        province = address[:2] + '0000'
        city = address[:4] + '00'
        print(addr_dict[province], addr_dict[city], addr_dict[address])
        return True
    else:
        return False


def check_city(city_code):
    code = int(city_code)
    city = {11: "北京", 12: "天津", 13: "河北", 14: "山西", 15: "内蒙古", 21: "辽宁", 22: "吉林", 23: "黑龙江 ", 31: "上海",
            32: "江苏", 33: "浙江", 34: "安徽", 35: "福建", 36: "江西", 37: "山东", 41: "河南", 42: "湖北", 43: "湖南",
            44: "广东", 45: "广西", 46: "海南", 50: "重庆", 51: "四川", 52: "贵州", 53: "云南", 54: "西藏", 61: "陕西",
            62: "甘肃", 63: "青海", 64: "宁夏", 65: "新疆", 71: "台湾", 81: "香港", 82: "澳门", 91: "国外"}
    if code in city:
        print(city[code])
        return True
    else:
        return False


def check_id(identity_code):
    length = len(identity_code)
    addr = identity_code[:6]
    city = identity_code[:2]
    if length == 15:
        year = identity_code[6:8]
        month = identity_code[8:10]
        day = identity_code[10:12]
        code = '-1'
        gender = identity_code[-1]
    elif length == 18:
        year = identity_code[6:10]
        month = identity_code[10:12]
        day = identity_code[12:14]
        code = identity_code[-1]
        gender = identity_code[-2]
    else:
        print('身份证号长度错误')
        return False
    # if not check_city(city):
    #     print('城市编码错误')
    #     return False
    if not check_addr(addr):
        print('地理位置编码错误')
        return False
    if not check_year(year):
        print('出生年份错误')
        return False
    if not check_month(month):
        print('出生月份错误')
        return False
    if not check_day(day, month, year):
        print('出生日期错误')
        return False
    if int(gender) % 2 == 0:
        print('女')
    else:
        print('男')
    if code != '-1':
        factors = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 0]
        validate_code = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        weight_sum = 0
        index = 0
        for ch in identity_code:
            Ai = int(ch)
            Wi = factors[index]
            weight_sum += Ai * Wi
            index += 1
        modal = weight_sum % 11
        if not code == validate_code[modal]:
            print('校验码错误, 应为%s' % validate_code[modal])
            return False
    return True


if __name__ == '__main__':
    while True:
        identity = input('请输入身份证号：')
        if check_id(identity):
            print('身份证号正确')

