import os
import requests
import re  # 正则表达式
import pprint
import json
from tqdm import tqdm
from bs4 import BeautifulSoup

'''
    爬取bilibili视频：张雪峰
'''


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'referer': 'https://space.bilibili.com/28152637/channel/seriesdetail?sid=1259590'    # 跳过防盗链
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
    url_list = ['https://www.bilibili.com/video/BV1nC4y1b7ns/?spm_id_from=333.999.0.0',
                'https://www.bilibili.com/video/BV1jK411J7uW/?spm_id_from=333.999.0.0',
                'https://www.bilibili.com/video/BV1za4y1a7Nd/?spm_id_from=333.999.0.0',
                'https://www.bilibili.com/video/BV1Cf4y1R7AF/?spm_id_from=333.999.0.0',
                'https://www.bilibili.com/video/BV15C4y1b7MX/?spm_id_from=333.999.0.0',
                'https://www.bilibili.com/video/BV1vT4y1E7NV/?spm_id_from=333.999.0.0',
                'https://www.bilibili.com/video/BV13f4y1R7tv/?spm_id_from=333.999.0.0',
                'https://www.bilibili.com/video/BV1uf4y1R7pV/?spm_id_from=333.999.0.0',
                'https://www.bilibili.com/video/BV1Yi4y1V7Cx/?spm_id_from=333.999.0.0',
                'https://www.bilibili.com/video/BV1Ak4y167ra/?spm_id_from=333.999.0.0',
                'https://www.bilibili.com/video/BV1Vi4y1V7pn/?spm_id_from=333.999.0.0',
                'https://www.bilibili.com/video/BV1Up4y1U7of/?spm_id_from=333.999.0.0',
                'https://www.bilibili.com/video/BV1rf4y117F1/?spm_id_from=333.999.0.0',
                'https://www.bilibili.com/video/BV1Tv41167EN/?spm_id_from=333.999.0.0',
                'https://www.bilibili.com/video/BV1mf4y127hS/?spm_id_from=333.999.0.0',
                'https://www.bilibili.com/video/BV1qt4y1177Z/?spm_id_from=333.999.0.0',
                'https://www.bilibili.com/video/BV1Qf4y1m7BZ/?spm_id_from=333.999.0.0']
    save_path = "D:/dataset/spider_dataset/zhangxuefeng/"

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
        # os.rename("%s/output_%s.mp4" % (save_path, str(i)), "%s/%s.mp4" % (save_path, str(title)))


        # break