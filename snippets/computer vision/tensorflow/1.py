import os

from basic import physical_devices

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import mnist

# physical_devices = tf.config.experimental.list_physical_devices('GPU')
# tf.config.experimental.set_memory_growth(physical_devices[0], True)


(x_train, y_train), (x_test, y_test) = mnist.load_data()
# shape of x_train = (60000, 28, 28), and now we are flatten x_train
x_train = x_train.reshape(-1, 28*28).astype("float32") / 255.0  #normalde 0 255 arası, normalize ettik 0 1 arası oldu
x_test = x_test.reshape(-1, 28*28).astype("float32") / 255.0

# sequential api of keras (very conveinent, not very flexible) => we can only map one input to one output
# Sequential API’de sadece "input → hidden layers → output" şeklinde sıralı bir akış vardır.
# fully connected layer(layers.Dense)  and 512 nodes (units neurons)
# Parametre	Açıklama
# units	Nöron sayısı (zorunlu).
# activation	Aktivasyon fonksiyonu (örn: 'relu', 'sigmoid', 'softmax').
# use_bias	Bias terimi kullanılsın mı? Varsayılan: True.
# kernel_initializer	Ağırlıkların başlangıç değerini belirler ('glorot_uniform' varsayılan).
# bias_initializer	Biasların başlangıç değerini belirler ('zeros' varsayılan).
# kernel_regularizer	L1 veya L2 gibi düzenleme yöntemlerini eklemek için.

model = keras.Sequential(
    [
        keras.Input(shape=(28*28)),  # print(model.summary()) yazdırabilmek için,  MNIST gibi 28x28 görüntüleri vektör haline getirerek modele vermek için kullanılır.
        # eğer olmazsa böyle diyor: ValueError: This model has not yet been built. Build the model first by calling `build()` or by calling the model on a batch of data.
        layers.Dense(512, activation='relu'),
        layers.Dense(256, activation='relu'),
        layers.Dense(10) # we are gonna use softmax on the output bu that is gonna be done inside the loss funciton
    ])

# print(model.summary())
# import sys
# sys.exit()

# şöyle de yapılır:
model = keras.Sequential()
# print(model.summary())  satır satır bakabilirsin böylece
model.add(keras.Input(shape=(28*28,)))
model.add(layers.Dense(256, activation='relu', name='layer'))
model.add(layers.Dense(10))

# normalde -1 olacaktı yani sonuncu layer output  layer ama bununla isteiğimiz satırı alabiliriz predict yapmak için (debuggging)
model = keras.Model(inputs=model.inputs, outputs=[model.layers[-2].output])
# model = keras.Model(inputs=model.inputs, outputs=[model.get_layer("layer").output])
# tüm layerları al:
# model = keras.Model(inputs=model.inputs, outputs=[layer.output for layer in model.layers])



feature = model.predict(x_train)



# Functional API (a bit more flexible)  yukarıdaki ile aynı
inputs = keras.Input(shape=(28*28,))
x = layers.Dense(512, activation='relu', name="first_layer")(inputs)
x = layers.Dense(256, activation='relu', name="second_layer")(x)
outputs = layers.Dense(10, activation='softmax')(x)
model = keras.Model(inputs=inputs, outputs=outputs)


# print(model.summary())
# import sys
# sys.exit()





# Eğer modelin çıkış katmanı softmax kullanıyorsa, from_logits=False olmalıdır. Çünkü softmax zaten olasılıkları hesaplar.

#Fonksiyon	Etiket Formatı	Kullanım Alanı
# SparseCategoricalCrossentropy	Tek sayı (integer) (örn. [0], [1])	Etiketler integer formatında olduğunda
# CategoricalCrossentropy	One-hot encoded (örn. [1,0,0], [0,1,0])	Etiketler one-hot encoded formatında olduğunda
model.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=False), # softmax activation olmadığından true ,  eğer sparse olmazsa one hot encoding oluyor
    # functional api ile yazında softmax var, ondan false yaptık (default değeri false)
    optimizer=keras.optimizers.Adam(lr=0.001),
    metrics=['accuracy']
)
# Keras'ta modelin başarımını ölçmek için farklı metrikler de kullanabilirsiniz.
#
# Metrik	Açıklama
# accuracy	Doğru tahminlerin oranı (genel kullanım için).
# binary_accuracy	İkili sınıflandırma (0 ve 1) için doğruluk.
# sparse_categorical_accuracy	Integer etiketli çok sınıflı sınıflandırmalar için doğruluk.
# categorical_accuracy	One-hot encoded etiketlerle çok sınıflı sınıflandırmalar için doğruluk.
# precision	Modelin pozitif sınıfı tahmin etme başarısını ölçer.
# recall	Modelin tüm gerçek pozitifleri yakalama başarısını ölçer.
# f1_score	Precision ve Recall'ün dengeli bir kombinasyonunu ölçer.

model.fit(x_train, y_train, batch_size=32, epochs=5, verbose=2) #2 seferde 1 yaz
model.evaluate(x_test, y_test, batch_size=32, verbose=2)























