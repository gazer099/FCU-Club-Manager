# http://www.cnblogs.com/Finley/p/5946000.html
import math
import random

from sklearn.metrics import mean_squared_error

random.seed(0)


def rand(a, b):
    return (b - a) * random.random() + a


def make_matrix(m, n, fill=0.0):
    mat = []
    for i in range(m):
        mat.append([fill] * n)
    return mat


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


class BPNeuralNetwork:
    def __init__(self):
        self.input_n = 0
        self.hidden_n = 0
        self.output_n = 0
        self.input_cells = []
        self.hidden_cells = []
        self.output_cells = []
        self.input_weights = []
        self.output_weights = []
        self.input_correction = []
        self.output_correction = []

    def setup(self, ni, nh, no):
        self.input_n = ni + 1
        self.hidden_n = nh
        self.output_n = no
        # init cells
        self.input_cells = [1.0] * self.input_n
        self.hidden_cells = [1.0] * self.hidden_n
        self.output_cells = [1.0] * self.output_n
        # init weights
        self.input_weights = make_matrix(self.input_n, self.hidden_n)
        self.output_weights = make_matrix(self.hidden_n, self.output_n)
        # random activate
        for i in range(self.input_n):
            for h in range(self.hidden_n):
                self.input_weights[i][h] = rand(-0.2, 0.2)
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                self.output_weights[h][o] = rand(-2.0, 2.0)
        # init correction matrix
        self.input_correction = make_matrix(self.input_n, self.hidden_n)
        self.output_correction = make_matrix(self.hidden_n, self.output_n)

    def predict(self, inputs):
        # activate input layer
        for i in range(self.input_n - 1):
            self.input_cells[i] = inputs[i]
        # activate hidden layer
        for j in range(self.hidden_n):
            total = 0.0
            for i in range(self.input_n):
                total += self.input_cells[i] * self.input_weights[i][j]
            self.hidden_cells[j] = sigmoid(total)
        # activate output layer
        for k in range(self.output_n):
            total = 0.0
            for j in range(self.hidden_n):
                total += self.hidden_cells[j] * self.output_weights[j][k]
            self.output_cells[k] = sigmoid(total)
        return self.output_cells[:]

    def back_propagate(self, case, label, learn, correct):
        # feed forward
        self.predict(case)
        # get output layer error
        output_deltas = [0.0] * self.output_n
        for o in range(self.output_n):
            error = label[o] - self.output_cells[o]
            output_deltas[o] = sigmoid_derivative(self.output_cells[o]) * error
        # get hidden layer error
        hidden_deltas = [0.0] * self.hidden_n
        for h in range(self.hidden_n):
            error = 0.0
            for o in range(self.output_n):
                error += output_deltas[o] * self.output_weights[h][o]
            hidden_deltas[h] = sigmoid_derivative(self.hidden_cells[h]) * error
        # update output weights
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                change = output_deltas[o] * self.hidden_cells[h]
                self.output_weights[h][o] += learn * change + correct * self.output_correction[h][o]
                self.output_correction[h][o] = change
        # update input weights
        for i in range(self.input_n):
            for h in range(self.hidden_n):
                change = hidden_deltas[h] * self.input_cells[i]
                self.input_weights[i][h] += learn * change + correct * self.input_correction[i][h]
                self.input_correction[i][h] = change
        # get global error
        error = 0.0
        for o in range(len(label)):
            error += 0.5 * (label[o] - self.output_cells[o]) ** 2
        return error

    def train(self, cases, labels, limit=10000, learn=0.05, correct=0.1):
        for j in range(limit):
            error = 0.0
            for i in range(len(cases)):
                label = labels[i]
                case = cases[i]
                error += self.back_propagate(case, label, learn, correct)

    def test(self):
        # cases = [
        #     [0, 0],
        #     [0, 1],
        #     [1, 0],
        #     [1, 1],
        # ]
        # labels = [[0], [1], [1], [0]]

        cases = [
            [
                0.23999999999999999, 0.17000000000000001, 0.21499999999999997, 0.023629078131263036,
                0.00055833333333333299, 0.28069999999999995, 6],
            [
                0.27000000000000002, 0.13, 0.20000000000000001, 0.070000000000000007, 0.0049000000000000007,
                0.089800000000000005, 2],
            [
                1.0, 0.10000000000000001, 0.43599999999999994, 0.23420219184855354, 0.054850666666666673,
                3.6742000000000004, 15],
            [
                0.26000000000000001, 0.11, 0.20249999999999999, 0.057608593109014568, 0.0033187500000000005,
                0.17730000000000001, 4],
            [
                0.23000000000000001, 0.17000000000000001, 0.20750000000000002, 0.024874685927665497,
                0.00061874999999999994, 0.17470000000000002, 4],
            [
                0.20000000000000001, 0.19, 0.19500000000000001, 0.0050000000000000044, 2.5000000000000045e-05,
                0.076100000000000001, 2],
            [
                0.28000000000000003, 0.17999999999999999, 0.2233333333333333, 0.041899350299921798,
                0.0017555555555555569, 0.15489999999999998, 3],
            [
                0.20000000000000001, 0.16, 0.17999999999999999, 0.020000000000000004, 0.00040000000000000018,
                0.065600000000000006, 2],
            [
                0.20999999999999999, 0.19, 0.20000000000000001, 0.009999999999999995, 9.999999999999991e-05,
                0.080199999999999994, 2]
        ]
        labels = [[0.470360878012484], [0.23814641808937209], [1.0], [0.93629862345500392], [0.42914720350543589],
                  [0.22188003803067258], [0.42714232565830268], [0.44363606299863584], [0.39264602538134019]]

        self.setup(7, 15, 1)
        self.train(cases, labels, 10000, 0.05, 0.1)
        predict_all = []
        for case in cases:
            output = self.predict(case)
            predict_all.append(output)
            print(output)
        print('MSE :', mean_squared_error(labels, predict_all))


if __name__ == '__main__':
    nn = BPNeuralNetwork()
    nn.test()
