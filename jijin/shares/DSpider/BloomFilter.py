#!/usr/bin/python26
# encoding=utf-8

'''
    BloomFilter去重器
    1、数据量不大时，可以直接放在内存里面进行去重，例如python可以使用set()进行去重。
    2、当去重数据需要持久化时可以使用redis的set数据结构。
    3、当数据量再大一点时，可以用不同的加密算法先将长字符串压缩成 16/32/40 个字符，再使用上面两种方法去重；
    4、当数据量达到亿（甚至十亿、百亿）数量级时，内存有限，必须用“位”来去重，才能够满足需求。Bloomfilter就是将去重对象映射到几个内存“位”，通过几个位的 0/1值来判断一个对象是否已经存在。
    5、然而Bloomfilter运行在一台机器的内存上，不方便持久化（机器down掉就什么都没啦），也不方便分布式爬虫的统一去重。如果可以在Redis上申请内存进行Bloomfilter，以上两个问题就都能解决了。
'''

import redis
from hashlib import md5


class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap) & ret


class BloomFilter(object):
    def __init__(self, host='localhost', port=6379, password='123456', db=0, blockNum=1, key='bloomfilter'):
        '''
            初始化Bloom过滤器
        :param host: Redis的host
        :param port: Redis的端口
        :param db: 选择哪个db
        :param blockNum: 位数组的长度，一个块大概是9千万字节，如果有更多的字节可以增加
        :param key: 往Redis中保存的键
        '''
        self.server = redis.Redis(host=host, port=port, password=password, db=db)
        self.bit_size = 1 << 31  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.key = key
        self.blockNum = blockNum
        self.hashFuc = []
        for seed in self.seeds:
            self.hashFuc.append(SimpleHash(self.bit_size, seed))

    def isContains(self, str_input):
        if not str_input:
            return False
        m5 = md5()
        m5.update(str_input.encode("utf-8"))
        str_input = m5.hexdigest()
        ret = True

        name = self.key + str(int(str_input[0:2], base=16) % self.blockNum)
        for f in self.hashFuc:
            loc = f.hash(str_input)
            ret = ret & self.server.getbit(name, loc)

        return ret

    def insert(self, str_input):
        m5 = md5()
        m5.update(str_input.encode("utf-8"))
        str = m5.hexdigest()
        name = self.key + str(int(str_input[0:2], base=16) % self.blockNum)
        for f in self.hashFuc:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 1)


def main():
    bf = BloomFilter(host='192.168.100.130')
    if bf.isContains('http://www.baidu.com'):  # 判断字符串是否存在
        print("exists!")
        # print
        # 'exists!'
    else:
        print("not exists!")
        bf.insert('http://www.baidu.com')


if __name__ == '__main__':
    # main()
    print(len(str(md5("Hello".encode("utf-8")))))
