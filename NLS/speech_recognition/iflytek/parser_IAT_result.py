import json

'''
    解析IAT_tingxie输出文件为汉字文本
'''

dict = {}

with open("d:/data/iat_tingxie/reco_result.txt", 'r', encoding='utf-8') as fo:
    filename = ""
    content = ["begin"]
    for line in fo.readlines():
        line = line.rstrip("\n")    # 去掉最后的\n
        if line.endswith(".wav"):
            filename = line
            content = []
        elif line.__contains__("call success!,data is:"):
            content.append(line)
            dict[filename] = content

with open("D:/data/iat_tingxie/reco_text.txt", 'w', encoding="utf-8") as fw:
    for k in dict.keys():
        # print(k, type(dict[k]), dict[k])
        filename = k
        text = ""
        for content in dict[k]:
            jsonArr = json.loads(content[59:])
            for jArr in jsonArr:
                text = text + jArr["cw"][0]["w"]

        # print(filename, text)
        fw.write(filename + " " + text + "\n")

print("parser finished")