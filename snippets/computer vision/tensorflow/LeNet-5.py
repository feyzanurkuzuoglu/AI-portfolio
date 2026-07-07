import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# LeNet-5 Modeli
model = Sequential([
    # C1 - İlk Konvolüsyon Katmanı (6 filtre, 5x5 kernel, tanh aktivasyonu)
    Conv2D(filters=6, kernel_size=(5, 5), activation='tanh', input_shape=(32, 32, 1)),
    MaxPooling2D(pool_size=(2, 2)),  # S2 - İlk Havuzlama Katmanı (2x2)

    # C3 - İkinci Konvolüsyon Katmanı (16 filtre, 5x5 kernel, tanh aktivasyonu)
    Conv2D(filters=16, kernel_size=(5, 5), activation='tanh'),
    MaxPooling2D(pool_size=(2, 2)),  # S4 - İkinci Havuzlama Katmanı (2x2)

    Flatten(),  # C5 - Fully Connected (Tam Bağlantılı Katmana Geçiş)

    # C5 - Tam Bağlantılı Katman (120 nöron, tanh aktivasyonu)
    Dense(120, activation='tanh'),

    # F6 - Tam Bağlantılı Katman (84 nöron, tanh aktivasyonu)
    Dense(84, activation='tanh'),

    # Çıkış Katmanı (10 nöron, Softmax aktivasyonu)
    Dense(10, activation='softmax')
])

# Modelin özetini yazdıralım
model.summary()

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

from tensorflow.keras.datasets import mnist
import numpy as np

# MNIST veri setini yükleyelim
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Veriyi normalize edelim ve 4D hale getirelim (Batch_size, Height, Width, Channels)
x_train = x_train.astype(np.float32) / 255.0
x_test = x_test.astype(np.float32) / 255.0
x_train = np.expand_dims(x_train, axis=-1)  # (60000, 28, 28) → (60000, 28, 28, 1)
x_test = np.expand_dims(x_test, axis=-1)

# Görselleri 32x32 boyutuna yükseltelim (LeNet-5 32x32 giriş alır)
x_train = tf.image.resize(x_train, [32, 32])
x_test = tf.image.resize(x_test, [32, 32])

# Modeli eğit
model.fit(x_train, y_train, epochs=10, batch_size=32, validation_data=(x_test, y_test))

test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"Test Doğruluğu: {test_acc:.4f}")

