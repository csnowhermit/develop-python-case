#!/usr/bin/python26
# encoding=utf-8

import codecs
import time

'''
    数据存储器：将爬取到的数据写入文件
    数据存储：每条记录为一行，<td><tr>url</tr><tr>title</tr><tr>summary</tr></td>
'''


class DataOutput(object):
    def __init__(self):
        # 生成文件按照当前时间命名
        self.filepath = 'baike_%s.html' % (time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))
        self.output_head(self.filepath)
        self.datas = []

    def store_data(self, data):
        if data is None:
            return
        self.datas.append(data)  # 对文件进行带缓存写入
        if len(self.datas) > 10:
            self.output_html(self.filepath)

    def output_head(self, path):
        '''
        将HTML头写进去
        :return:
        '''
        fout = codecs.open(path, 'w', encoding='utf-8')
        fout.write("<html>")
        fout.write("<body>")
        fout.write("<table>")
        fout.close()

    def output_html(self, path):
        '''
        将数据写入HTML文件中
        :param path: 文件路径
        :return:
        '''
        fout = codecs.open(path, 'a', encoding='utf-8')
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data['url'])
            fout.write("<td>%s</td>" % data['title'])
            fout.write("<td>%s</td>" % data['summary'])
            fout.write("</tr>")
            self.datas.remove(data)
        fout.close()

    def ouput_end(self, path):
        '''
        输出HTML结束
        :param path: 文件存储路径
        :return:
        '''
        fout = codecs.open(path, 'a', encoding='utf-8')
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()
