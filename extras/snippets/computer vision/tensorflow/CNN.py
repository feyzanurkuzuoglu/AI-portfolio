import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, regularizers
from tensorflow.keras.datasets import cifar10

# CIFAR-10 dataset
# 50k training image, 10k test images and 32x32 pixels RGB ==> 3 channels

(x_train, y_train), (x_test, y_test) = cifar10.load_data()
#computing in float64 is unnecessary computation, float32ye çeviriyoruz, for normalization /255
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0


# sequential API
model = keras.Sequential(
    [
       keras.Input(shape=(32, 32, 3)),
        layers.Conv2D(32, 3, padding='valid', activation='relu'),
        # filters=32 → 32 adet konvolüsyon filtresi kullanılır.
        # kernel_size=(3,3) → Her filtre 3×3 boyutunda olacak.
        # activation='relu' → Aktivasyon fonksiyonu olarak ReLU kullanılıyor.
        # input_shape=(64,64,3) → 64×64 boyutunda ve 3 kanallı (RGB) bir görüntü işlenecek.
        # padding= valid yazmaya gerek yoktu
        layers.MaxPooling2D(pool_size=(2, 2)),
        # MaxPooling2D(pool_size=(2,2), strides=None, padding="valid") varsayılan değerler
        # strides=None → Varsayılan olarak strides=pool_size olur (stride otomatik olarak (2,2) seçilir). strides=(2,2)
        layers.Conv2D(64, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(128, 3, activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10)
        # Keras varsayılan olarak activation=None kullanır.
        # Bu durumda, aktivasyon fonksiyonu uygulanmaz ve doğrusal (linear) bir çıktı üretilir.
    ]
)
# functional API
# accuracy arttırmak için batch normalization ekleyeceğiz, accuracy artacak ama overfitting var, regularization yapacağız
# batch normalization sequental ile de yapılırdı

# 📌 Batch Normalization (Batch Norm), sinir ağlarında eğitim sürecini hızlandırmak ve daha kararlı hale getirmek için kullanılan bir tekniktir.
# ✅ Katmanlar arasında verileri normalize eder.
# ✅ Gradient Descent’in daha düzgün çalışmasını sağlar.
# ✅ Overfitting’i azaltarak genelleme yeteneğini artırır.

# Eğitim sırasında, her katmandaki ağırlıkların dağılımı sürekli değişir (Internal Covariate Shift problemi).
# Bu durum modelin öğrenmesini zorlaştırır ve optimizasyonu yavaşlatır.
#
# 📌 Örnek Problem:
#
# İlk epoch’ta giriş dağılımı (ortalama = 0, standart sapma = 1)
# 10.epoch’ta dağılım kaydı (ortalama = 5, standart sapma = 10)
# 20.epoch’ta dağılım yine değişti...
# Bu sürekli değişim, ağın öğrenmesini zorlaştırır ve training süresini uzatır.
#
# Çözüm: Batch Normalization, her minibatch'in dağılımını normalize ederek bu problemi çözer.

def my_model():
    inputs = keras.Input(shape=(32, 32, 3))
    x = layers.Conv2D(32, 3, padding='same', kernel_regularizer=regularizers.l2(0.01))(inputs)
    x = layers.BatchNormalization()(x)
    x = keras.activations.relu(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Conv2D(64, 3, padding='same', kernel_regularizer=regularizers.l2(0.01))(x)
    x = layers.BatchNormalization()(x)
    x = keras.activations.relu(x)
    x = layers.Conv2D(128, 3, padding='same', kernel_regularizer=regularizers.l2(0.01))(x)
    x = layers.BatchNormalization()(x)
    x = keras.activations.relu(x)
    x = layers.Flatten()(x)
    x = layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.01))(x)
    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(10)(x)
    model = keras.Model(inputs=inputs, outputs=outputs)
    return model


model = my_model()

model.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True), #outputta softmax olmadığında true oluyor
    optimizer=keras.optimizers.Adam(lr=3e-4),
    metrics=['accuracy']
)


# model.fit(), modeli eğitim verisiyle (training data) eğitmek için kullanılır.
# model.evaluate(), eğitilmiş modelin test verisi üzerinde performansını değerlendirmek için kullanılır. epochs parametresi burada kullanılmaz!
# Eğitim (fit()) sırasında model çoklu epoch boyunca öğrenir, ancak değerlendirme (evaluate()) sırasında sadece bir kez test seti üzerinde doğruluk ve kayıp ölçülür.
# model.evaluate() modelin eğitilmesini sağlamaz, sadece test verisinde doğruluğu ve kaybı ölçer. Ağırlıklar güncellenmez.
model.fit(x_train, y_train, batch_size=64, epochs=10, verbose=2)
model.evaluate(x_test, y_test, batch_size=64, verbose=2)

