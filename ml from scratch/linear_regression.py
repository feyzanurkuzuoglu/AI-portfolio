import numpy as np

 # m = training examples, n = number of features
 # y: R^(1xm), X is R^(nxm), w is R^(nx1)

class LinearRegression():
     def __init__(self):
         self.learning_rate = 0.01
         self.total_iterations = 10000


     def yhat(self, X, w): # yhat = w1x1 + w2x2 + w3x3 + ...
         return np.dot(w.T, X)

     def loss(self, yhat, y):
         L = 1/self.m * np.sum(np.power(yhat - y, 2))
         return L

     def gradient_descent(self, w, X, y, yhat):
         # (n x m) dot  (1 x m).T
         dLdw = 2/self.m * np.dot(X, (yhat - y).T)

         w = w - self.learning_rate * dLdw
         return w

     def main(self, X, y):
         x1 = np.ones((1, X.shape[1]))
         X = np.append(X, x1, axis=0)

         self.m = X.shape[1]
         self.n = X.shape[0]

         w = np.zeros((self.n, 1))

         for it in range(self.total_iterations+1):
             yhat = self.yhat(X,w)
             loss = self.loss(yhat, y)


             if it % 2000 == 0:
                 print(f"Cost at iteration {it} is {loss}")

             w = self.gradient_descent(w, X, y, yhat)

         return w

if __name__ == "__main__":
    X = np.random.randn(1, 5000)
    y = 3 * X + np.random.randn(1,5000)*0.1
    regression = LinearRegression()
    w = regression.main(X, y)