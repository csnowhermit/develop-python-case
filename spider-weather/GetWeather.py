from bs4 import BeautifulSoup
import requests, time, random, socket, csv
import http.client


# 获取请求网址的完整HTML代码
def htmlcontent(url, data=None):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }   # request 的请求头
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url, headers=header, timeout=timeout)   # 请求url地址，获得返回response信息
            rep.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print('3:', e)
            time.sleep(random.choice(range(8, 15)))

        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print('6:', e)
            time.sleep(random.choice(range(5, 15)))
    return rep.text   # 返回的Html全部代码

# 过滤筛选有用数据
def weatherdata(html_text):
    data_al = []
    bs = BeautifulSoup(html_text, "html.parser")   # 创建BeautifulSoup对象并以html.parser方式解析
    li = bs.body.find('div', {'id': '7d'}).find('ul').find_all('li')   # 根据前端HTML代码的标签获取具体天气数据

    for data in li:
        temp = []
        date = data.find('h1').string
        inf = data.find_all('p')
        weather = inf[0].string   # 天气
        temperature_highest = inf[1].find('span').string    # 最高温度
        temperature_low = inf[1].find('i').string   # 最低温度
        temp.append(date)   # 添加日期
        temp.append(weather)    # 添加天气
        temp.append(temperature_low)    # 添加最低温度
        temp.append(temperature_highest)    # 添加最高温度
        data_al.append(temp)  # 数据全部储存在一个列表中
    return data_al


# 把数据写入本地文件
def writedata(data, name):
    with open(name, 'a', errors='ignore', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)


if __name__ == '__main__':
    url = 'http://www.weather.com.cn/weather/101280101.shtml'   # 获取天气数据的网址
    html = htmlcontent(url)    # 获取网页信息
    result = weatherdata(html)    # 解析网页信息，拿到需要的数据
    print(result)
    # writedata(result, 'd:/天气test.csv')  # 数据写入到 csv文档中
