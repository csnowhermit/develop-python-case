import os
import time
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import traceback


# 配置chrome 防止出现滑块验证
service = ChromeService(executable_path="D:/opt/chromedriver-win32/chromedriver.exe")
options = webdriver.ChromeOptions()  # 配置chrome 防止出现滑块验证
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument('--disable-blink-features=AutomationControlled')
prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()  # 窗口最大化，防止元素重叠无法点击

driver.get("http://www.taobao.com/")

# 获取登录按钮并点击
login_button1 = driver.find_element(By.XPATH,
                                    '/html/body/div[3]/div[2]/div[2]/div[2]/div[5]/div/div[2]/div[1]/a[1]')
login_button1.click()

# 点击登录按钮，会跳转至登录页面需要重定位活跃窗口
driver.switch_to.window(driver.window_handles[-1])
driver.implicitly_wait(15)  # 等待网页加载

# 获取用户名、密码input以及登录button
username_input = driver.find_element(By.XPATH,
                                     '/html/body/div/div[2]/div[3]/div/div/div/div[2]/div/form/div[1]/div[2]/input')
password_input = driver.find_element(By.XPATH,
                                     '/html/body/div/div[2]/div[3]/div/div/div/div[2]/div/form/div[2]/div[2]/input')
login_button2 = driver.find_element(By.XPATH,
                                    '/html/body/div/div[2]/div[3]/div/div/div/div[2]/div/form/div[4]/button')

# 输入用户名密码并单击登录按钮
username_input.send_keys('username')
time.sleep(1)
password_input.send_keys('password')
time.sleep(1)
login_button2.click()

# 登录后会进行用户验证，需要手机淘宝点击确认登陆
# input("请进行手机验证，验证通过后按回车继续脚本")

# 进入我的淘宝页面
my_tb = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/ul[2]/li[2]/div[1]/a')
my_tb.click()
print("已进入我的淘宝页面")

# 进入订单页面
driver.implicitly_wait(15)
goods_form_page = driver.find_element(By.XPATH, '//*[@id="bought"]')
goods_form_page.click()
print("已进入订单页面")

# 展示5s后关闭
time.sleep(5)

# 关闭Chrome
driver.quit()
