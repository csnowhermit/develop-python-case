#!/usr/bin/python26
#encoding=utf-8

import redis

cli = redis.Redis(host='192.168.100.130', port=6379, password='123456')
print(cli.get('mldn'))

