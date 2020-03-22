import tensorflow as tf
import numpy as np

'''
    TensorFlow矩阵运算：从文件读取矩阵
'''

'''
    从文件中读取矩阵
    :return 返回list，单项为每行的内容
'''
def readFile(filenames):
    result = []
    f = open(filenames, 'r')
    for line in f.readlines():
        line = line.rstrip("\n")
        result.append(line)

    return result

'''
    将list转换成矩阵
    :return 返回形成的矩阵
'''
def convertList2Matrix(list):
    result = []
    for line in list:
        numList = line.split(",")
        newList = []
        for v in numList:
            newList.append(float(v))
        result.append(newList)
    return np.matrix(result)

def main(argv=None):
    sourceFile = "./testData/model.csv"                # 输入数据
    weightParamFile = "./testData/weightParam.csv"    # 权重参数
    bias = 10    # 偏置量

    x = readFile(sourceFile)        # 得到的是list
    w = readFile(weightParamFile)

    x = convertList2Matrix(x)
    w = convertList2Matrix(w)

    x = tf.constant(x, dtype=tf.float32)
    w = tf.constant(w, dtype=tf.float32)

    with tf.Session() as sess:
        result = tf.matmul(x, w)
        print(sess.run(result) + bias)


if __name__ == '__main__':
    tf.app.run()

