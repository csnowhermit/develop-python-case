# -*- coding:utf-8 -*-

from sklearn.model_selection import train_test_split
from NLP.textCategory.bayes.bayes_train import *
from NLP.textCategory.bayes.bayes_test import get_newest_model
from NLP.textCategory.decisionTree.decisionTree_train import buildFeatureMat, decisionTreeClassifier_model_path


'''
    从文件中读取模型并进行分类
'''

test_data = get_dataset()  # 加载原始文本，新切词为测试数据
test_mat, test_labels = buildFeatureMat(test_data, keywords)  # 构建测试矩阵及label
train_set_tmp, test_set, train_label_tmp, test_label = train_test_split(test_mat, test_labels, test_size=0.99)

'''
    测试分类树
'''
def test_decisionTree(model_file):
    clf = joblib.load(model_file)
    score = clf.score(test_set, test_label)  # 在测试数据上测试效果
    print("模型准确率：", score)

def main():
    model_file = get_newest_model(decisionTreeClassifier_model_path)
    print(model_file)
    test_decisionTree(model_file)

if __name__ == '__main__':
    main()