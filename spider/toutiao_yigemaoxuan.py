import os
import re
import json
import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'referer': 'https://www.toutiao.com/video/7140231584904416520/?app=news_article_lite&timestamp=1668684550&share_token=2d7f8f7e-7e96-4df1-a4b2-f4c280d2c523&source=m_redirect&wid=1668684611677'    # 跳过防盗链
}

# url = "https://v9-web.toutiaovod.com/b2f04b9275756b59b9d1be0a82d0972b/637629b8/video/tos/cn/tos-cn-ve-15/f14c17df9dc44095a34d21b460fb9a7d/?a=24&ch=0&cr=0&dr=0&lr=unwatermarked&net=5&cd=0%7C0%7C0%7C0&cv=1&br=1042&bt=1042&cs=0&ds=3&ft=WbaUMqBrffPdHK~2N12NvAq-antLjrKYbjJARkaF1n0SejVhbHr&mime_type=video_mp4&qs=0&rc=Zjc5OTg1Z2U2aDllOzc3PEBpM3QzOGQ6ZmRpNjMzNGkzM0A2LV4zYTQ0NTQxLi5iLWE2YSMtbTMtcjRnM2NgLS1kLTBzcw%3D%3D&l=2022111719313301015022201422B6BB99&btag=10000"
url = "https://www.toutiao.com/video/7140231584904416520/?app=news_article_lite&timestamp=1668684550&share_token=2d7f8f7e-7e96-4df1-a4b2-f4c280d2c523&source=m_redirect&wid=1668684611677"



'''
    请求数据
'''
def send_request(url):
    response = requests.get(url=url, headers=headers)
    return response

if __name__ == '__main__':
    html_data = send_request(url).text
    html_bs = BeautifulSoup(html_data, features="lxml")
    # print(html_data)
    # title = html_bs.title.text  # 前言_哔哩哔哩_bilibili
    # print(title)
    html_bs

    # 解析出视频的链接
    # json_data = re.findall('<script>window\.__playinfo__=(.*?)</script>', html_data)[0]
    json_data = re.findall('<video class="" autoplay="" tabindex="2" mediatype="video"', html_data)[0]
    # print(json_data)  # json_data 字符串
    json_data = json.loads(json_data)

# html_bs = BeautifulSoup(response)
# print(html_bs)

# with open(os.path.join("./", "toutiao.mp4"), mode='wb') as f:
#     f.write(response)
#     print('正在保存视频数据')



