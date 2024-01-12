import os
import time
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import traceback

'''
    获取指定网页并保存为PDF
'''

def scroll_and_load_images(driver, scroll_step=300, sleep_time=3):
    # 获取窗口高度
    window_height = driver.execute_script("return window.innerHeight")
    print("窗口高度:", window_height)

    # 初始化滚动位置
    scroll_pos = 0

    # 逐步滚动页面
    while True:
        # 滚动到下一个位置
        print("滚动条当前位置:", scroll_pos)
        scroll_pos += scroll_step
        driver.execute_script(f"window.scrollTo(0, {scroll_pos});")
        time.sleep(sleep_time)  # 等待加载

        # 检查是否滚到底部
        scroll_pos_js = driver.execute_script("return window.pageYOffset;")
        if scroll_pos_js + window_height >= driver.execute_script("return document.body.scrollHeight"):
            # 尝试滚动一点超出底部，确保触发所有懒加载行为
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(sleep_time)
            # 再次检查是否到底部，结束滚动循环
            if scroll_pos_js == driver.execute_script("return window.pageYOffset;"):
                break

if __name__ == '__main__':
    # 设置ChromeDriver的服务
    service = ChromeService(executable_path="D:/opt/chromedriver-win32/chromedriver.exe")

    # 设置Chrome的选项
    chrome_options = webdriver.ChromeOptions()

    # 支持无界面的headless模式
    chrome_options.add_argument("--headless")

    # 为确保打印样式，可设定浏览器宽高
    chrome_options.add_argument("--window-size=1920,1080")

    # 初始化WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 要访问的网址
    # url = 'https://prodev.jd.com/mall/active/4CbNduaE946DLsfz59RSkiu1FVUy/index.html'    # 京东链接
    # url = "https://item.taobao.com/item.htm?id=36830875489"    # 淘宝商品链接
    # url = "https://shop108156093.taobao.com/?spm=pc_detail.27183998.202202.1.660f7dd6UZToTP"    # 淘宝店铺
    # url = "https://detail.tmall.com/item.htm?id=717423847853"    # 天猫商品链接
    url = "https://shouwu.tmall.com/shop/view_shop.htm?spm=pc_detail.27183998"    # 天猫店铺
    save_path = "D:/data/spider/"

    # 访问网页
    driver.get(url)
    title = driver.title
    print("title:", title)

    savefile = os.path.join(save_path, "%s.pdf" % title.replace("/", ""))

    # 等待页面加载完毕
    time.sleep(3)    # 请根据实际情况调整等待时间

    # 滚动页面以确保所有懒加载的图像都加载了
    scroll_and_load_images(driver, scroll_step=300, sleep_time=3)

    # 将当前网页保存为PDF
    params = {
        'printBackground': True,
        # 'pageRanges': '1-',  # 页码范围，也可以指定多个范围；写1-表示保存所有页
        'path': savefile
    }

    # 存储PDF
    try:
        result = driver.execute_cdp_cmd("Page.printToPDF", params)
        if result.get('data'):
            with open(savefile, 'wb') as f:
                f.write(base64.b64decode(result['data']))
            print(f'网页已保存为PDF: {savefile}')
        else:
            print("PDF生成失败，未获取到数据。")
    except Exception as e:
        print("打印PDF时发生错误:", traceback.format_exc())

    # 关闭Chrome
    driver.quit()

