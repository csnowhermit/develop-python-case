import os

st_path = "D:/workspace/openSourceModel/ASRT_SpeechRecognition/dataset/ST-CMDS-20170001_1-OS/"

details = open("D:/data/iat_tingxie/metadata.txt", 'w', encoding='utf-8')
text = open("D:/data/iat_tingxie/text.txt", 'w', encoding='utf-8')

for file in os.listdir(st_path):
    if file.endswith(".metadata"):
        content = ""
        try:
            with open(st_path + file, 'r', encoding='utf-8') as fo:
                for line in fo.readlines():
                    line = line.rstrip("\n")
                    if line.__contains__("LBN"):
                        content = content + line + ","
                    elif line.__contains__("SEX"):
                        content = content + line + ","
                    elif line.__contains__("AGE"):
                        content = content + line + ","
                    elif line.__contains__("ACT"):
                        content = content + line + ","
                    elif line.__contains__("BIR"):
                        content = content + line
        except Exception:
            pass
        print(content)
        details.write(content + "\n")
    elif file.endswith(".txt"):
        try:
            with open(st_path + file, 'r', encoding='utf-8') as fo:
                line = fo.readline()
                text.write(file + " " + line + "\n")
        except Exception:
            pass
    else:
        pass