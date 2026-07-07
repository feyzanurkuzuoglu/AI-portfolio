import numpy as np

"""
| Özellik     | Normal Equation        | Gradient Descent                     |
| ----------- | ---------------------- | ------------------------------------ |
| Hesaplama   | Kapalı form çözüm      | İteratif optimizasyon                |
| Karmaşıklık | $O(n^3)$               | $O(kn^2)$, k = iterasyon sayısı      |
| Büyük veri  | Verimsiz               | Daha uygun                           |
| Parametre   | Öğrenme oranı gerekmez | Öğrenme oranı seçilmeli              |
| Doğruluk    | Tam çözüm              | Yaklaşık çözüm (iterasyonlara bağlı) |


en uygun doğruyu bulmayı sağlar. 
"""

# X: (training_examples, features)
# Y: (training_examples, 1)
# output w: (features, 1)

def linear_regression_normal_equation(X,y):
    ones = np.ones((X.shape[0], 1))
    X = np.append(ones, X, axis=1)
    # Normal Equation’un güvenli versiyonunu hesaplıyor
    W = np.dot(np.linalg.pinv(np.dot(X.T, X)), np.dot(X.T, y))
    return W

# y_pred = XW olacak. W: [intercept, katsayı]

if __name__ == "__main__":
    X = np.array([[1,2,3]]).T
    y = np.array([-1,0,1])
    print(linear_regression_normal_equation(X,y))

    X1 = np.random.randn(5000,1)
    y1 = 5*X1 + np.random.randn(5000,1)*0.1
    W1 = linear_regression_normal_equation(X1, y1)
    print(W1)