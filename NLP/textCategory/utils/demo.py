
import time

s = "直行通道过去，右转有自助售票机。"

print(str(time.time()).replace('.', '') + "@" + hex(s.__hash__()))

list = []
with open("../kdata/intention_answer.txt", encoding="utf-8", errors="ignore") as fo:
    for line in fo.readlines():
        arr = line.strip().split("\t")
        ars = arr[2].split("|")
        for a in ars:
            list.append(a)

print(len(list))
print(list)
print(len(set(list)))
print(set(list))

answers = []
slist = set(list)
for s in slist:
    answers.append(s[3:])

print(len(answers))
print(answers)
print(len(set(answers)))
print(set(answers))