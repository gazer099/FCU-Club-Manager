# http://www.cnblogs.com/Finley/p/5953122.html
import tensorflow as tf
import numpy as np
from sklearn.metrics import mean_squared_error


def make_layer(inputs, in_size, out_size, activate=None):
    weights = tf.Variable(tf.random_normal([in_size, out_size]))
    basis = tf.Variable(tf.zeros([1, out_size]) + 0.1)
    result = tf.matmul(inputs, weights) + basis
    if activate is None:
        return result
    else:
        return activate(result)


class BPNeuralNetwork:
    def __init__(self):
        self.session = tf.Session()
        self.loss = None
        self.optimizer = None
        self.input_n = 0
        self.hidden_n = 0
        self.hidden_size = []
        self.output_n = 0
        self.input_layer = None
        self.hidden_layers = []
        self.output_layer = None
        self.label_layer = None
        self.mse = None

    def __del__(self):
        self.session.close()

    def setup(self, ni, nh, no):
        # set size args
        self.input_n = ni
        self.hidden_n = len(nh)  # count of hidden layers
        self.hidden_size = nh  # count of cells in each hidden layer
        self.output_n = no
        # build input layer
        self.input_layer = tf.placeholder(tf.float32, [None, self.input_n])
        # build label layer
        self.label_layer = tf.placeholder(tf.float32, [None, self.output_n])
        # build hidden layers
        in_size = self.input_n
        out_size = self.hidden_size[0]
        inputs = self.input_layer
        self.hidden_layers.append(make_layer(inputs, in_size, out_size, activate=tf.nn.relu))
        for i in range(self.hidden_n - 1):
            in_size = out_size
            out_size = self.hidden_size[i + 1]
            inputs = self.hidden_layers[-1]
            self.hidden_layers.append(make_layer(inputs, in_size, out_size, activate=tf.nn.relu))
        # build output layer
        self.output_layer = make_layer(self.hidden_layers[-1], self.hidden_size[-1], self.output_n)

    def train(self, cases, labels, limit=10000, learn_rate=0.05):
        self.loss = tf.reduce_mean(
            tf.reduce_sum(tf.square((self.label_layer - self.output_layer)), reduction_indices=[1]))
        self.optimizer = tf.train.GradientDescentOptimizer(learn_rate).minimize(self.loss)
        initer = tf.global_variables_initializer()
        # do training
        self.session.run(initer)
        for i in range(limit):
            self.session.run(self.optimizer, feed_dict={self.input_layer: cases, self.label_layer: labels})

    def predict(self, case):
        return self.session.run(self.output_layer, feed_dict={self.input_layer: case})

    def test(self, cases_test, labels_test):
        # x_data = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        # y_data = np.array([[0, 1, 1, 0]]).transpose()
        # test_data = np.array([[0, 1]])
        # self.setup(2, [10, 5], 1)
        # self.train(x_data, y_data)
        # print(self.predict(test_data))

        predict_all = self.predict(cases_test)  # Direct predict entire array
        self.mse = mean_squared_error(labels_test, predict_all)
        print('MSE :', self.mse)
        return predict_all

    def save_model(self, model_path):
        saver = tf.train.Saver()
        save_path = saver.save(self.session, model_path)
        print("Save to path: ", save_path)

    def load_model(self, model_path):
        saver = tf.train.Saver()
        saver.restore(self.session, model_path)

if __name__ == '__main__':
    nn = BPNeuralNetwork()
    nn.test()
