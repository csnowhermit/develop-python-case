#!/usr/bin/python26
# encoding=utf-8

'''
    淘宝商品信息抓取
'''

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import UnexpectedAlertPresentException
import time,unittest,re

def auto_login():
    username = input("username: ")
    password = input("password: ")  # 从键盘输入密码，但这样不安全
    # password=getpass.getpass("password: ")    #getpass模块貌似只能在命令行下跑

    # 登录页面
    brower = webdriver.PhantomJS(executable_path="D:/Anaconda3/phantomjs-2.1.1-windows/bin/phantomjs.exe")
    brower.get("https://login.taobao.com")

    # 进入用户名密码模式
    brower.find_element_by_xpath('/html/body/div/div[2]/div[3]/div/div/div[2]/div[4]/div/div[5]/a').click()
    brower.find_element_by_xpath('/html/body/div/div[2]/div[3]/div/div/div[2]/div[3]/form/div[2]/span').click()

    # 会员名/邮箱/手机号
    brower.find_element_by_id('TPL_username_1').send_keys(username)
    brower.find_element_by_id('TPL_password_1').click()  # 输完用户名后点击密码框
    brower.find_element_by_id('TPL_password_1').send_keys(password)
    result = brower.find_element_by_id('J_SubmitStatic').click()  # 点登录按钮

    # 如果无返回，则登录成功；否则是出现了滑块验证
    if result == None:
        print("登录成功")
    else:
        time.sleep(2)

        # 处理滑块验证的情况
        dragger = brower.find_element_by_id('nc_1_n1z')  # 滑块定位
        print(dragger)
        action = ActionChains(brower)

        for index in range(500):
            try:
                action.drag_and_drop_by_offset(dragger, 500, 0).perform()  # 平行移动鼠标，此处直接设一个超出范围的值，这样拉到头后会自动报错从而结束这个动作
            except UnexpectedAlertPresentException:
                break
            time.sleep(1)  # 滑动滑块的时候报错了就sleep 1秒，之后再试

        # 滑完滑块之后重新点击登录按钮
        brower.find_element_by_id('J_SubmitStatic').click()
        print("Login Finished")

def main():
    auto_login()




if __name__ == '__main__':
    main()