import requests
from lxml import etree

'''
    静态网页爬取
'''

# 要爬取的网页链接
url = 'https://www.hrrsj.com/zhichang/gongsijianjie/27244.html'

# 设置请求头，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 使用requests发送HTTP GET请求
response = requests.get(url, headers=headers)

# 检查请求是否成功
if response.status_code == 200:
    # 解析网页内容
    tree = etree.HTML(response.content)

    # 获取网页标题
    title_element = tree.xpath('//title/text()')
    title = title_element[0] if title_element else 'No Title Found'
    title = str(title).replace("/", "").replace("\\", "")
    print("title:", title)

    # 获取整个页面的HTML字符串
    html_content = etree.tostring(tree, encoding='utf-8').decode('utf-8')

    # 将标题和内容一起保存到本地文件
    with open('%s.txt' % title, 'w', encoding='utf-8') as file:
        file.write(f"Title: {title}\n\n")
        file.write(html_content)
    print("标题和内容已保存到本地文件。")
else:
    print("请求失败，状态码：", response.status_code)
