import os
import os.path as osp
import argparse

from spider.util.bilibili_spider import Bilibili_Spider
from spider.util.tools import download_video


def main(args):
    bilibili_spider = Bilibili_Spider(args.uid, args.save_dir, args.save_by_page, args.time)
    url_list, title_list = bilibili_spider.get()
    # if args.detailed:
    #     bilibili_spider.get_detail()
    save_path = "D:/testdata/helaoshishuojingji"
    for url, title in zip(url_list, title_list):
        download_video(url, title, save_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--uid', type=str, default='493805437')
    parser.add_argument('--save_dir', type=str, default='json')
    parser.add_argument('--save_by_page', action='store_true', default=False)
    parser.add_argument('--time', type=int, default=2, help='waiting time for browser.get(url) by seconds')
    parser.add_argument('--detailed', action='store_true', default=False)
    args = parser.parse_args()
    print(args)

    main(args)