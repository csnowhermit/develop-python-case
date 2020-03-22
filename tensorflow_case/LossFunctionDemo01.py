import tensorflow as tf

'''
    自定义损失函数：使神经网络优化的结果更接近于实际的需求；
    Demo：在商品销量预测中，如果预测值>实际销量，商家损失的是成本；
    预测试<实际销量，商家损失的是利润；
    大多数情况下，成本和利润不会严格相等，或者，利润远远高于成本；
    例：某商品，成本1元，利润10元，则损失函数应为：
    Loss(x, y)=tf.reduce_sum(f(x, y)),
        if x > y : a * (x - y), a=10;
        if x <= y : b * (y - x), b=1;
    x：实际销量；
    y：预测销量；
    a：利润；
    b：成本；
'''

x = tf.constant([1.0, 2.0, 3.0, 4.0], name='x')
y = tf.constant([4.0, 3.0, 2.0, 1.0], name='y')

sess = tf.InteractiveSession()

print(sess.run(tf.greater(x, y)))
print(sess.run(tf.where(tf.greater(x, y), x, y)))

sess.close()

