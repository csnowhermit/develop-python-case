# -*- coding:utf-8 -*-

import os
from sklearn.externals import joblib
from NLP.textCategory.bayes.bayes_train import get_dataset, split_train_and_test_set, multinamialNB_save_path, bernousNB_save_path

'''
    从文件读取模型并进行分类
'''

test_data = get_dataset()
train_set_tmp, train_label_tmp, test_set, test_label = split_train_and_test_set(test_data, 0.0)

'''
    获取最新的模型
'''
def get_newest_model(model_path):
    if os.path.exists(model_path):
        # 按文件最后修改时间排序，reverse=True表示降序排序
        filelist = sorted(os.listdir(model_path), key=lambda x: os.path.getctime(os.path.join(model_path, x)), reverse=True)
        return os.path.join(model_path, filelist[0])



'''
    测试多项式分类器
'''
def test_bayes(model_file):
    clf = joblib.load(model_file)
    predict = clf.predict(test_set)

    count = 0
    for left, right, tset in zip(predict, test_label, test_set):
        print(left, "-->", right, "-->", tset)
        if left == right:
            count += 1
    print(model_file, "准确率：", count / len(test_label))



def main():
    # test_bayes(get_newest_model(multinamialNB_save_path))
    test_bayes(get_newest_model(bernousNB_save_path))
    # print(get_newest_model(multinamialNB_save_path))
    # print(get_newest_model(bernousNB_save_path))

if __name__ == '__main__':
    main()