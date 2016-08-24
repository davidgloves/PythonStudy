#!/usr/bin/env python
# encoding: utf-8

"""
@author: david
@license: Apache Licence 
@contact: davidguy127@gmail.com
@site: 
@software: PyCharm
@file: employee.py
@time: 8/24/16 8:33 PM
"""

"""

北京市税务局官网
http://gs.tax861.gov.cn/zxl.htm

1 不超过1500元的 3%
2 超过1500元至4500元的部分 10%
3 超过4500元至9000元的部分 20%
4 超过9000元至35000元的部分 25%
5 超过35000元至55000元的部分 30%
6 超过55000元至80000元的部分 35%
7 超过80000元的部分 45%


养老 8%
医疗 2%
失业 城镇户口0.2%，农村户口0%
公积金 12%

如果单位缴费基数为最低则养老与失业是一样的，其它的保险基数是一样的

"""
MedicalKey = 'medical'
EndowmentKey = 'endowment'
UnemploymentKey = 'unemployment'
HousingfundKey = 'housing'
TaxKey = 'tax'
SalaryKey = 'salary'


def get_result(*, salary, bases, rates):
    """
    :param salary: the salary of the employee
    :param bases: the all bases of Social insurance, Housing fund and tax
    :param rates: the rates of all Social insurance and Hosing fund
    :return: a tuple of all count result, include medical, endowment, unemployment insurance and housing fund
    sum tax, and the finally salary
    """

    medical_insurance = bases[MedicalKey] * rates[MedicalKey]
    endowment_insurance = bases[EndowmentKey] * rates[EndowmentKey]
    unemployment_insurance = bases[UnemploymentKey] * rates[UnemploymentKey]

    housing_fund = bases[HousingfundKey] * rates[HousingfundKey]

    tax_base = salary - medical_insurance - endowment_insurance - \
               unemployment_insurance - housing_fund - bases[TaxKey]

    sum_tax = 0

    tax_rate1 = 0.03
    tax_rate2 = 0.1
    tax_rate3 = 0.2
    tax_rate4 = 0.25
    tax_rate5 = 0.3
    tax_rate6 = 0.35
    tax_rate7 = 0.45

    level1 = tax_rate1 * 1500
    level2 = tax_rate2 * (4500 - 1500) + level1
    level3 = tax_rate3 * (9000 - 4500) + level2
    level4 = tax_rate4 * (35000 - 9000) + level3
    level5 = tax_rate5 * (55000 - 35000) + level4
    level6 = tax_rate6 * (80000 - 55000) + level5

    if tax_base < 0:
        print('无需缴纳个人所得税')
    elif 0 < tax_base <= 1500:
        sum_tax = tax_base * tax_rate1
    elif 1500 < tax_base <= 4500:
        sum_tax = level1 + (tax_base - 1500) * tax_rate2
    elif 4500 < tax_base <= 9000:
        sum_tax = level2 + (tax_base - 4500) * tax_rate3
    elif 9000 < tax_base <= 35000:
        sum_tax = level3 + (tax_base - 9000) * tax_rate4
    elif 35000 < tax_base <= 55000:
        sum_tax = level4 + (tax_base - 35000) * tax_rate5
    elif 55000 < tax_base <= 80000:
        sum_tax = level5 + (tax_base - 55000) * tax_rate6
    elif 1500 < tax_base <= 4500:
        sum_tax = level6 + (tax_base - 80000) * tax_rate7

    return {MedicalKey: medical_insurance, EndowmentKey: endowment_insurance, UnemploymentKey: unemployment_insurance,
            HousingfundKey: housing_fund, TaxKey: sum_tax, SalaryKey: tax_base - sum_tax + bases[TaxKey]}


def valid_input(prompt, default, not_zero=False):
    """
    :param prompt: user input prompt
    :param default: if user input nothing then use the default value
    :return: the default value or input value
    """
    number = input(prompt)
    if not number.strip():
        number = 0.0
    else:
        number = float(number)
    if not number > 0:
        if not_zero:
            return valid_input(prompt, default, not_zero)
        else:
            return default
    else:
        return number


def input_info():
    bases = {}
    rates = {}

    idcard = input('是否农村户口(y/n):')

    salary = valid_input('您的税前工资是：', 0, True)
    bases[MedicalKey] = valid_input('医保缴费基数(默认为税前工资)：', salary)
    bases[EndowmentKey] = valid_input('养老保险缴费基数(默认为税前工资)：', salary)
    if idcard == 'n':
        bases[UnemploymentKey] = valid_input('失业保险缴费基数(默认为税前工资)：', salary)
    else:
        bases[UnemploymentKey] = 0
    bases[HousingfundKey] = valid_input('住房公积金缴费基数(默认为税前工资)：', salary)
    bases[TaxKey] = valid_input('个税缴纳基础(默认为3500)：', 3500)

    rates[MedicalKey] = valid_input('医保缴费比率(默认为2%)：', 0.02)
    rates[EndowmentKey] = valid_input('养老保险缴费比率(默认为8%)：', 0.08)
    if idcard == 'n':
        rates[UnemploymentKey] = valid_input('失业保险缴费比率(默认为0.2%)：', 0.002)
    else:
        rates[UnemploymentKey] = 0
    rates[HousingfundKey] = valid_input('住房公积金缴费比率(默认为12%)：', 0.12)

    results = get_result(salary=salary, bases=bases, rates=rates)
    print_results(results)
    print("\n", "-" * 70, "\n", "-" * 70)


def print_results(results):
    print("养老保险     :", results[EndowmentKey])
    print("医疗保险     :", results[MedicalKey])
    print("失业保险     :", results[UnemploymentKey])
    print("住房公积金   :", results[HousingfundKey])
    print("个人所得税   :", results[TaxKey])
    print("实际个人所得 :", results[SalaryKey])


if __name__ == '__main__':
    print('下面为个人实际工资计算器，请依提示输入相关信息。\n\n')
    while True:
        input_info()