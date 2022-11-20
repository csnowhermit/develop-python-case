import os
import requests
import re  # 正则表达式
import pprint
import json
from tqdm import tqdm
from bs4 import BeautifulSoup

'''
    爬取bilibili视频：汤山老王
'''


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'referer': 'https://www.bilibili.com/video/BV1ea411H7h7/?spm_id_from=333.337.search-card.all.click'    # 跳过防盗链
}


'''
    请求数据
'''
def send_request(url):
    response = requests.get(url=url, headers=headers)
    return response

'''
    解析网页数据  
'''
def get_video_data(html_data):
    # 提取视频的标题
    # title = re.findall('<span class="title">(.*?)</span>', html_data)[0]
    # title = re.findall('<div class="cur-list">(.*?)</div>', html_data)
    # print(title)

    # 提取视频对应的json数据
    json_data = re.findall('<script>window\.__playinfo__=(.*?)</script>', html_data)[0]
    # print(json_data)  # json_data 字符串
    json_data = json.loads(json_data)
    # pprint.pprint(json_data)

    # 提取音频的url地址
    audio_url = json_data['data']['dash']['audio'][0]['backupUrl'][0]
    print('解析到的音频地址:', audio_url)

    # 提取视频画面的url地址
    video_url = json_data['data']['dash']['video'][0]['backupUrl'][0]
    print('解析到的视频地址:', video_url)

    video_data = [audio_url, video_url]
    return video_data

'''
    请求数据并保存
'''
def save_data(file_name, audio_url, video_url, save_path):
    print('正在请求音频数据')
    audio_data = send_request(audio_url).content
    print('正在请求视频数据')
    video_data = send_request(video_url).content
    with open(os.path.join(save_path, "%s.mp3" % file_name), mode='wb') as f:
        f.write(audio_data)
        print('正在保存音频数据')
    with open(os.path.join(save_path, "%s.mp4" % file_name), mode='wb') as f:
        f.write(video_data)
        print('正在保存视频数据')

'''
    音视频合并
'''
def merge_data(video_name, save_path):
    # print('音视频合成开始:', video_name)
    # ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac -strict experimental output.mp4
    COMMAND = f'D:/opt/ffmpeg-5.1.2-essentials_build/bin/ffmpeg.exe -i %s/%s.mp4 -i %s/%s.mp3 -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 %s/output_%s.mp4' % (save_path, str(video_name), save_path, str(video_name), save_path, str(video_name))
    print(COMMAND)
    os.system(COMMAND)
    # print('音视频合成结束:', video_name)


if __name__ == '__main__':
    url_list = ['https://www.bilibili.com/video/BV1ea411H7h7/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1fu411C7pd/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV133411w7Eh/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1Yq4y1Y7nm/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1MB4y1W76U/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1UY411N7k2/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1S5411U7hG/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1WL4y177sF/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1544y1T7b4/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1344y1P7fb/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1LF411W7Ak/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1WP4y1u7ML/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1Dd4y1d7Du/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1wZ4y1z7wm/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1ZS4y1N7cX/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1ft4y1b749/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1tr4y1M7H7/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1VY4y1L7JW/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1wP4y1Z7LP/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1fY411N75d/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1Jf4y1Z7fk/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1jV4y1J7yB/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1td4y1A74R/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1oF411u72G/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1tZ4y1C7iw/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1aW4y1q7SF/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1yY411t7CJ/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1bg411F7dF/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1wh411x7EP/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1sr4y1879m/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1ZP4y1N7yh/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1KS4y1672F/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1654y1f7gQ/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1iB4y1y7WL/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV19g411A7oc/?spm_id_from=333.337.search-card.all.click',
                'https://www.bilibili.com/video/BV1FZ4y1b7j7/?spm_id_from=333.337.search-card.all.click'
               ]
    save_path = "D:/dataset/spider_data/tangshanlaowang"

    for i in tqdm(range(len(url_list))):
        html_data = send_request(url_list[i]).text
        html_bs = BeautifulSoup(html_data, features="lxml")
        # print(html_data)
        title = html_bs.title.text    # 前言_哔哩哔哩_bilibili
        print(i, "\t", title)

        # video_data = get_video_data(html_data)
        #
        # save_data(str(i), video_data[0], video_data[1], save_path)

        # merge_data(i, save_path)

        # 改名
        os.rename("%s/output_%s.mp4" % (save_path, str(i)), "%s/%s.mp4" % (save_path, str(title)))


        # break