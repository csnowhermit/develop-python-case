import sys
import difflib

labelsDict = {}    # 正确的标注
with open("D:/workspace/openSourceModel/ASRT_SpeechRecognition/datalist/thchs30/精简版标注数据-汉字.txt", 'r', encoding='utf-8') as fo:
    for line in fo.readlines():
        line = line.rstrip("\n")
        arr = line.split(" ")
        labelsDict[arr[0]] = arr[1]


predictDict = {}    # 识别到的
with open("D:/data/iat_tingxie/reco_text.txt", 'r', encoding='utf-8') as fo:
    for line in fo.readlines():
        line = line.rstrip("\n")
        arr = line.split(" ")
        arr[0] = arr[0][arr[0].rfind('/')+1:]
        # print(arr[0], arr[1])
        predictDict[arr[0]] = arr[1]

print(labelsDict)
print(predictDict)


for k in labelsDict.keys():
    v1 = labelsDict.get(k)
    v2 = predictDict.get(k+".wav")

    if v1 is not None and v2 is not None:
        d = difflib.Differ()
        diff = d.compare(v1, v2)
        print(",".join(diff))
    # print(difflib.ndiff(v1, v2))




