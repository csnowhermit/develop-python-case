# -*- coding:utf-8 -*-

import os

'''
    截取全国所有火车站
    信息来源：https://kyfw.12306.cn/otn/resources/js/framework/station_name.js
'''

def genStationList():
    provinces = ['北京', '天津', '上海', '重庆', '河北', '山西',
                 '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽',
                 '福建', '江西', '山东', '河南', '湖北', '湖南',
                 '广东', '海南', '四川', '贵州', '云南', '陕西',
                 '甘肃', '青海', '台湾', '内蒙古', '内蒙', '广西',
                 '西藏', '宁夏', '新疆', '香港', '澳门']

    station_names = []

    for p in provinces:
        station_names.append(p)

    with open("../kdata/all_station.txt", encoding="utf-8") as fo:
        for line in fo.readlines():
            arr = line.strip().split("|")
            station_names.append(arr[1].replace(' ', ''))

    with open("../kdata/others.txt", encoding="utf-8", mode="w") as fo:
        for station in station_names:
            fo.write(station + "\n")
            print(station)
    print("finished")
    return station_names

def main():
    station_names = genStationList()
    print(station_names)

if __name__ == '__main__':
    main()