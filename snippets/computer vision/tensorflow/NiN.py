import tensorflow as tf
from tensorflow.keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D, Activation, Input
from tensorflow.keras.models import Model


# 📌 Bu fonksiyon:
# ✔ 3×3 konvolüsyonla temel özellikleri çıkarır.
# ✔ Ardından 1x1 konvolüsyon kullanarak mikro MLP katmanları ekler.

# **NiN Blok Fonksiyonu**
def nin_block(x, num_channels):
    x = Conv2D(num_channels, kernel_size=(3,3), padding='same', activation='relu')(x)
    x = Conv2D(num_channels, kernel_size=(1,1), padding='same', activation='relu')(x)
    x = Conv2D(num_channels, kernel_size=(1,1), padding='same', activation='relu')(x)
    return x

def build_nin(input_shape=(224, 224, 3), num_classes=10):
    inputs = Input(shape=input_shape)

    # **1. NiN Blok**
    x = nin_block(inputs, 96)
    x = MaxPooling2D(pool_size=(3,3), strides=2, padding='same')(x)

    # **2. NiN Blok**
    x = nin_block(x, 256)
    x = MaxPooling2D(pool_size=(3,3), strides=2, padding='same')(x)

    # **3. NiN Blok**
    x = nin_block(x, 384)
    x = MaxPooling2D(pool_size=(3,3), strides=2, padding='same')(x)

    # **Global Average Pooling (GAP)**
    x = GlobalAveragePooling2D()(x)

    # **Tam Bağlantılı Katman (Softmax Çıkışı)**
    outputs = tf.keras.layers.Dense(num_classes, activation='softmax')(x)

    # **Modeli Tanımla**
    model = Model(inputs, outputs)
    return model

# **NiN Modelini Başlat**
nin_model = build_nin()

# **Modelin Özetini Yazdır**
nin_model.summary()
