import tensorflow as tf
import numpy as np

'''
    one_hot编码Demo：对标数据进行one_hot编码之后，计算矩阵计算
'''

# 输入数据，设计为：线路，站名，进站人数，出站人数
x = [['1', '西朗', 50, 60],
     ['1', '坑口', 40, 20],
     ['1', '花地湾', 60, 25],
     ['2', '公园前', 50, 40],
     ['3', '体育西路', 90, 80],
     ['3', '珠江新城', 90, 70],
     ['gf', '千灯湖', 40, 20],
     ['7', '汉溪长隆', 50, 20]]

# 参数比重
weights = [[0.2],
           [0.2],
           [0.3],
           [0.3]]

'''
    对指定列进行one_hot编码
    :param x: 源矩阵
    :param *p: 需要进行one_hot编码的列
'''
def getOne_hot(x, *p):
    x = np.mat(x)
    onehotDict = {}
    dictp = {}    # <k, v>：<矩阵的第几列, 编码后形成的0-1新列数>

    # 逐列对指定列的数据进行one_hot编码
    for i in p:
        isAllChar = True;    # 默认为全字符型标量，只有全字符的情况下maxValue才能从0开始编码，否则只能从len(arr)开始编码
        col = x[:, i]
        arr = np.array((col))

        # maxValue = len(arr)    # 从选中列的行数的最大值开始算
        maxValue = 0    # 从0开始填充，该列数据为标量数据，数据本身大小没什么意思，从0开始尽可能减少矩阵的稀疏程度，用len(arr)为初始值的缺点：对于全字符型的列，从0到len(arr)列都为空
        newArr = []
        dict = {}    # 存放标量数据与数值型数据的映射关系

        # 这层循环，将字符类型转换成数字类型
        for a in arr:
            s = str(a)
            start_index = 2
            end_index = len(s) - 2
            realValue = s[start_index: end_index]
            try:
                newArr.append(int(realValue))
                isAllChar = False    # 如果上一步强转没报错，说明存在数值型标量，这时只能从len(arr)开始编码
            except ValueError:
                # 如果替代字母的数字变量已经存在于原arr中，则maxValue+1，避免与已存在线路冲突
                # maxValue使用变长而不是定长的目的是：尽可能减少稀疏矩阵
                while maxValue in arr:
                    maxValue = maxValue + 1;
                newArr.append(maxValue)
                dict[realValue] = maxValue
                maxValue = maxValue + 1
                pass

        # print(newArr)
        CLASS = len(list(set(newArr)))
        # print(CLASS)

        with tf.Session() as sess:
            label1 = tf.constant(newArr)
            # print("before one hot: \n", sess.run(label1))
            tf.global_variables_initializer()
            if isAllChar is True:
                dictp[i] = maxValue
                b = tf.one_hot(label1, maxValue, 1, 0)
            else:
                dictp[i] = maxValue + len(arr) - 1
                b = tf.one_hot(label1, len(arr) + maxValue - 1, 1, 0)    # len(arr) + maxValue - 1，可以避免对不全是字符型标量的类型时，出现的最后一列全为0的情况
            # print("after one hot: \n", sess.run(b))

            one_hot_arr = sess.run(b)
            onehotDict[i] = one_hot_arr

        # print("已完成第 %d 列的编码" % i)
        # print(dict)
    return onehotDict, dictp

'''
    将one_hot编码后的矩阵完全替换原矩阵的相关列
    :param onehotDict: <在原矩阵的列下标, one_hot编码后的新矩阵>
    :param x: 原矩阵
'''
def newMat(onehotDict, x):
    x = np.mat(x)
    ret = np.zeros((x.shape[0], 1))    # 创建个空矩阵

    for i in range(x.shape[1]):
        if i in onehotDict:
            ret = np.column_stack((ret, onehotDict[i]))
        else:
            ret = np.column_stack((ret, x[:, i]))
            pass

    return np.delete(ret, 0, axis=1)    # 裁剪掉第一列，我们初始化为0的占位列

'''
    经过one_hot编码后，标量型数据会拆分为多列，故对应权重矩阵也需要进行行的扩张
    :param weightMatrix: 权重矩阵
    :param dictp: <矩阵的第几列, 编码后形成的0-1新列数>
'''
def expandWeightMatrix(weightMatrix, dictp):
    ret = []
    for i in range(len(weightMatrix)):
        if i in dictp:
            for j in range(dictp[i]):    # 如果对某一列进行one_hot编码了，该列就会被分化成多列，需要对多列进行权重的复制
                # print("======", i, j, weightMatrix[i], "======")
                ret.append(weightMatrix[i])
        else:
            ret.append(weightMatrix[i])
    return ret

def main():
    onehotDict, dictp = getOne_hot(x, 0, 1)
    ret = newMat(onehotDict, x)     # 形成的新的矩阵，该方法返回的矩阵可直接用来计算
    weightMat = expandWeightMatrix(weightMatrix=weights, dictp=dictp)

    final_result = np.mat(x)[:, [0, 1]]
    # 裁剪掉前两列
    # ret = np.delete(ret, 0, axis=1)
    # ret = np.delete(ret, 0, axis=1)

    with tf.Session() as sess:
        input = tf.constant(ret, dtype=tf.float32)
        weightMat = tf.constant(np.matrix(weightMat), dtype=tf.float32)

        result = tf.matmul(input, weightMat)
        result = sess.run(result)

        final_result = np.column_stack((final_result, np.mat(result)))
        print(final_result)


if __name__ == '__main__':
    main()