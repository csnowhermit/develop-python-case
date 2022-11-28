import os
import re
import sys
import time
import errno
import json
import warnings
import requests
from bs4 import BeautifulSoup


def mkdir_if_missing(dirname):
    """Creates dirname if it is missing."""
    if not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


def check_isfile(fpath):
    """Checks if the given path is a file."""
    isfile = os.path.isfile(fpath)
    if not isfile:
        warnings.warn('No file found at "{}"'.format(fpath))
    return isfile


def read_json(fpath):
    """Reads json file from a path."""
    with open(fpath, 'r') as f:
        obj = json.load(f)
    return obj


def write_json(obj, fpath):
    """Writes to a json file."""
    mkdir_if_missing(os.path.dirname(fpath))
    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=4, separators=(',', ': '), ensure_ascii=False) # 添加中文支持

'''
    通过url下载视频
'''
def download_video(url, title, save_path):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'referer': 'https://www.bilibili.com/video/BV1ea411H7h7/?spm_id_from=333.337.search-card.all.click'  # 跳过防盗链
    }

    response = requests.get(url=url, headers=headers)
    html_data = response.text
    html_bs = BeautifulSoup(html_data, features="lxml")

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

    # 下载
    print('正在请求音频数据')
    audio_data = requests.get(audio_url, headers=headers).content
    print('正在请求视频数据')
    video_data = requests.get(video_url, headers=headers).content
    with open(os.path.join(save_path, "tmp.mp3"), mode='wb') as f:
        f.write(audio_data)
        print('正在保存音频数据')
    with open(os.path.join(save_path, "tmp.mp4"), mode='wb') as f:
        f.write(video_data)
        print('正在保存视频数据')

    # 合并音频和视频
    COMMAND = f'D:/opt/ffmpeg-5.1.2-essentials_build/bin/ffmpeg.exe -i %s/tmp.mp4 -i %s/tmp.mp3 -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 %s/output_tmp.mp4' % (
    save_path, save_path, save_path)
    print(COMMAND)
    os.system(COMMAND)

    # 改名
    os.rename("%s/output_tmp.mp4" % (save_path), "%s/%s.mp4" % (save_path, str(title).replace("|", "").
                                                                                      replace(":", "")))
