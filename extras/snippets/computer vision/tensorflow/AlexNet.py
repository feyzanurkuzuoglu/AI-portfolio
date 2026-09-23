import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# AlexNet Modelini Oluşturma
model = Sequential([
    # C1 - İlk Konvolüsyon Katmanı (96 filtre, 11x11 kernel, stride=4, ReLU)
    Conv2D(filters=96, kernel_size=(11,11), strides=(4,4), activation='relu', input_shape=(227, 227, 3)),
    MaxPooling2D(pool_size=(3,3), strides=(2,2)),  # MaxPooling (3x3, stride=2)

    # C2 - İkinci Konvolüsyon Katmanı (256 filtre, 5x5 kernel, ReLU)
    Conv2D(filters=256, kernel_size=(5,5), padding="same", activation='relu'),
    MaxPooling2D(pool_size=(3,3), strides=(2,2)),

    # C3 - Üçüncü Konvolüsyon Katmanı (384 filtre, 3x3 kernel, ReLU)
    Conv2D(filters=384, kernel_size=(3,3), padding="same", activation='relu'),

    # C4 - Dördüncü Konvolüsyon Katmanı (384 filtre, 3x3 kernel, ReLU)
    Conv2D(filters=384, kernel_size=(3,3), padding="same", activation='relu'),

    # C5 - Beşinci Konvolüsyon Katmanı (256 filtre, 3x3 kernel, ReLU)
    Conv2D(filters=256, kernel_size=(3,3), padding="same", activation='relu'),
    MaxPooling2D(pool_size=(3,3), strides=(2,2)),

    Flatten(),  # Fully Connected Katmana Geçiş

    # FC6 - Tam Bağlantılı Katman (4096 nöron, ReLU)
    Dense(4096, activation='relu'),
    Dropout(0.5),  # Overfitting'i önlemek için Dropout ekleniyor

    # FC7 - Tam Bağlantılı Katman (4096 nöron, ReLU)
    Dense(4096, activation='relu'),
    Dropout(0.5),

    # FC8 - Çıkış Katmanı (1000 sınıflı Softmax aktivasyonu)
    Dense(1000, activation='softmax')
])

# Modelin özetini yazdıralım
model.summary()

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical

# CIFAR-10 veri setini yükleyelim
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# Veriyi normalize edelim (0-255 → 0-1)
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# Etiketleri one-hot encode yapalım
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# CIFAR-10 32x32 olduğu için, AlexNet'in beklediği 227x227 boyutuna yükseltelim
x_train = tf.image.resize(x_train, [227, 227])
x_test = tf.image.resize(x_test, [227, 227])

# Modeli eğit
model.fit(x_train, y_train, epochs=10, batch_size=32, validation_data=(x_test, y_test))

test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"Test Doğruluğu: {test_acc:.4f}")

