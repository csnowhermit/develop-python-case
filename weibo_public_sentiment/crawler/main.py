# -*- coding: utf-8 -*-

from weibo_public_sentiment.crawler import login
from weibo_public_sentiment.crawler import collectWeiboDataByKeyword
import urllib
import urllib2
import sys

uid = '18640376585'
psw = '89364013'

reload(sys)
sys.setdefaultencoding('utf8')    #这两句话用来修改系统默认编码

simLogin = login.WeiboLogin(uid, psw)
simLogin.login()

collectWeiboDataByKeyword.main();
