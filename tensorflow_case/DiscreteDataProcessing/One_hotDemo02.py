import tensorflow as tf
import numpy as np

'''
    one-hot编码
'''

# 输入数据：站ID，站名，所属线路
x = [[101, '西朗', '1'],
     [102, '公园前', '2'],
     [802, '沙园', '8'],
     [802, '沙园', 'gf'],
     [102, '公园前', '1']]

x = np.mat(x)

col = x[:, 2]    # [N * 1]矩阵
arr = np.array(col)

dict = {}        # 存储中文线路名与替换数字的对应关系
maxLine = 22    # 设置最大线路数量：线路为中文名的用该值替换，并递增
newArr = []
for a in arr:
    s = str(a)
    start_index = 2
    end_index = len(s) - 2
    lineValue = s[start_index: end_index]
    try:
        newArr.append(int(lineValue))
    except ValueError :
        newArr.append(maxLine)
        dict[lineValue] = maxLine
        maxLine = maxLine + 1
        pass

print(newArr)
CLASS = len(list(set(newArr)))
print(CLASS)

with tf.Session() as sess:
    label1 = tf.constant(newArr)
    print("before one hot: \n", sess.run(label1))
    tf.global_variables_initializer()
    b = tf.one_hot(label1, maxLine, 1, 0)
    print("after one hot: \n", sess.run(b))

    one_hot_Arr = sess.run(b)

    final_result = np.column_stack((x[:, [0, 1]], one_hot_Arr))
    print(final_result)