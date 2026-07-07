import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# VGG-16 Modelini Oluşturma
model = Sequential([
    # **Blok 1**
    Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same', input_shape=(224, 224, 3)),
    Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same'),
    MaxPooling2D(pool_size=(2,2), strides=(2,2)),

    # **Blok 2**
    Conv2D(filters=128, kernel_size=(3,3), activation='relu', padding='same'),
    Conv2D(filters=128, kernel_size=(3,3), activation='relu', padding='same'),
    MaxPooling2D(pool_size=(2,2), strides=(2,2)),

    # **Blok 3**
    Conv2D(filters=256, kernel_size=(3,3), activation='relu', padding='same'),
    Conv2D(filters=256, kernel_size=(3,3), activation='relu', padding='same'),
    Conv2D(filters=256, kernel_size=(3,3), activation='relu', padding='same'),
    MaxPooling2D(pool_size=(2,2), strides=(2,2)),

    # **Blok 4**
    Conv2D(filters=512, kernel_size=(3,3), activation='relu', padding='same'),
    Conv2D(filters=512, kernel_size=(3,3), activation='relu', padding='same'),
    Conv2D(filters=512, kernel_size=(3,3), activation='relu', padding='same'),
    MaxPooling2D(pool_size=(2,2), strides=(2,2)),

    # **Blok 5**
    Conv2D(filters=512, kernel_size=(3,3), activation='relu', padding='same'),
    Conv2D(filters=512, kernel_size=(3,3), activation='relu', padding='same'),
    Conv2D(filters=512, kernel_size=(3,3), activation='relu', padding='same'),
    MaxPooling2D(pool_size=(2,2), strides=(2,2)),

    # **Tam Bağlantılı (FC) Katmanlar**
    Flatten(),
    Dense(4096, activation='relu'),
    Dropout(0.5),
    Dense(4096, activation='relu'),
    Dropout(0.5),
    # Dense(1000, activation='softmax')  # ImageNet için 1000 sınıflı çıkış

# 🚀 **CIFAR-10 için 10 sınıfa uygun çıkış katmanı**
    Dense(10, activation='softmax')

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

# CIFAR-10 32x32 olduğu için, VGG-16'nın beklediği 224x224 boyutuna yükseltelim
x_train = tf.image.resize(x_train, [224, 224])
x_test = tf.image.resize(x_test, [224, 224])

# Modeli eğit
model.fit(x_train, y_train, epochs=10, batch_size=32, validation_data=(x_test, y_test))


test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"Test Doğruluğu: {test_acc:.4f}")
