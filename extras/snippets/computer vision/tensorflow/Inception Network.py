import tensorflow as tf
from tensorflow.keras.layers import Conv2D, MaxPooling2D, AveragePooling2D, concatenate, Input, Flatten, Dense, Dropout
from tensorflow.keras.models import Model

# **Inception Blok Fonksiyonu**
def inception_block(x, filters):
    f1, f2, f3, f4 = filters

    # **1x1 Konvolüsyon**
    conv1x1 = Conv2D(f1, (1,1), padding='same', activation='relu')(x)

    # **3x3 Konvolüsyon (Öncesinde 1x1 Kullanarak Kanal Sayısını Azaltıyoruz)**
    # Darboğaz (Bottleneck)
    conv3x3 = Conv2D(f2, (1,1), padding='same', activation='relu')(x)
    conv3x3 = Conv2D(f2, (3,3), padding='same', activation='relu')(conv3x3)

    # **5x5 Konvolüsyon (Öncesinde 1x1 Kullanarak Kanal Sayısını Azaltıyoruz)**
    conv5x5 = Conv2D(f3, (1,1), padding='same', activation='relu')(x)
    conv5x5 = Conv2D(f3, (5,5), padding='same', activation='relu')(conv5x5)

    # **3x3 MaxPooling + 1x1 Konvolüsyon**
    pool = MaxPooling2D((3,3), strides=(1,1), padding='same')(x)
    pool = Conv2D(f4, (1,1), padding='same', activation='relu')(pool)

    # **Tüm Filtreleri Birleştiriyoruz**
    output = concatenate([conv1x1, conv3x3, conv5x5, pool], axis=-1)
    return output

def build_inception_v1(input_shape=(224, 224, 3), num_classes=1000):
    inputs = Input(shape=input_shape)

    # **Başlangıç Katmanları**
    x = Conv2D(64, (7,7), strides=2, padding='same', activation='relu')(inputs)
    x = MaxPooling2D(pool_size=(3,3), strides=2, padding='same')(x)

    # **İlk Inception Blokları**
    x = inception_block(x, [64, 128, 32, 32])
    x = inception_block(x, [128, 192, 96, 64])
    x = MaxPooling2D(pool_size=(3,3), strides=2, padding='same')(x)

    # **Orta Seviye Inception Blokları**
    x = inception_block(x, [192, 208, 48, 64])
    x = inception_block(x, [160, 224, 64, 64])
    x = inception_block(x, [128, 256, 64, 64])
    x = MaxPooling2D(pool_size=(3,3), strides=2, padding='same')(x)

    # **Son Seviye Inception Blokları**
    x = inception_block(x, [256, 320, 128, 128])
    x = inception_block(x, [384, 384, 128, 128])

    # **Global Ortalama Havuzlama**
    x = AveragePooling2D(pool_size=(7,7))(x)
    x = Flatten()(x)
    x = Dropout(0.4)(x)

    # **Tam Bağlantılı Katman (Çıkış)**
    outputs = Dense(num_classes, activation='softmax')(x)

    # **Modeli Tanımla**
    model = Model(inputs, outputs)
    return model

# **Modeli Başlat**
inception_v1 = build_inception_v1()
inception_v1.summary()


# with auxiliary classifier
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense

def auxiliary_classifier(x, num_classes):
    x = GlobalAveragePooling2D()(x)  # Özellik haritasını sıkıştır
    x = Dense(512, activation='relu')(x)  # Ara tam bağlantılı katman
    x = Dense(num_classes, activation='softmax')(x)  # Softmax ile sınıflandırma
    return x


import tensorflow as tf
from tensorflow.keras.layers import Conv2D, MaxPooling2D, AveragePooling2D, GlobalAveragePooling2D, Flatten, Dense, Dropout, concatenate, Input
from tensorflow.keras.models import Model

# **Inception Blok**
def inception_block(x, filters):
    f1, f2, f3, f4 = filters

    conv1x1 = Conv2D(f1, (1,1), padding='same', activation='relu')(x)

    conv3x3 = Conv2D(f2, (1,1), padding='same', activation='relu')(x)
    conv3x3 = Conv2D(f2, (3,3), padding='same', activation='relu')(conv3x3)

    conv5x5 = Conv2D(f3, (1,1), padding='same', activation='relu')(x)
    conv5x5 = Conv2D(f3, (5,5), padding='same', activation='relu')(conv5x5)

    pool = MaxPooling2D((3,3), strides=(1,1), padding='same')(x)
    pool = Conv2D(f4, (1,1), padding='same', activation='relu')(pool)

    output = concatenate([conv1x1, conv3x3, conv5x5, pool], axis=-1)
    return output

# **Auxiliary Classifier (Ara Softmax)**
def auxiliary_classifier(x, num_classes):
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dense(num_classes, activation='softmax')(x)  # Ara softmax
    return x

# **Inception Network**
def build_inception_v1(input_shape=(224, 224, 3), num_classes=1000):
    inputs = Input(shape=input_shape)

    x = Conv2D(64, (7,7), strides=2, padding='same', activation='relu')(inputs)
    x = MaxPooling2D(pool_size=(3,3), strides=2, padding='same')(x)

    x = inception_block(x, [64, 128, 32, 32])
    x = inception_block(x, [128, 192, 96, 64])

    # **İlk Auxiliary Classifier**
    aux1 = auxiliary_classifier(x, num_classes)

    x = inception_block(x, [192, 208, 48, 64])
    x = inception_block(x, [160, 224, 64, 64])

    # **İkinci Auxiliary Classifier**
    aux2 = auxiliary_classifier(x, num_classes)

    x = inception_block(x, [256, 320, 128, 128])
    x = inception_block(x, [384, 384, 128, 128])

    x = GlobalAveragePooling2D()(x)
    x = Flatten()(x)
    x = Dropout(0.4)(x)
    outputs = Dense(num_classes, activation='softmax')(x)  # Ana softmax

    model = Model(inputs, [outputs, aux1, aux2])
    return model

# **Modeli Başlat**
inception_v1 = build_inception_v1()
inception_v1.summary()

