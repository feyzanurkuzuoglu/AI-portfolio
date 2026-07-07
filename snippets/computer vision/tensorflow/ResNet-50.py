import tensorflow as tf
from tensorflow.keras.layers import Conv2D, BatchNormalization, Activation, Add, Dense, MaxPooling2D, GlobalAveragePooling2D, Input
from tensorflow.keras.models import Model



# Katman No	Katman Türü	Çıkış Boyutu
# 1	Conv2D (7×7, 64 filtre, stride=2)	112×112×64
# 2	MaxPooling (3×3, stride=2)	56×56×64
# 3	3 x Residual Block (64, 64, 256)	56×56×256
# 4	4 x Residual Block (128, 128, 512)	28×28×512
# 5	6 x Residual Block (256, 256, 1024)	14×14×1024
# 6	3 x Residual Block (512, 512, 2048)	7×7×2048
# 7	Global Average Pooling	1×1×2048
# 8	Dense (1000 sınıf, softmax)	1000



# **Residual Block Fonksiyonu**
def residual_block(x, filters, kernel_size=3, stride=1):
    shortcut = x  # Kısa yol bağlantısı

    # **1x1 Konvolüsyon**
    x = Conv2D(filters, (1,1), strides=stride, padding='same')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    # **3x3 Konvolüsyon**
    x = Conv2D(filters, (kernel_size, kernel_size), strides=1, padding='same')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    # **1x1 Konvolüsyon**
    x = Conv2D(filters * 4, (1,1), strides=1, padding='same')(x)
    x = BatchNormalization()(x)

    # Y = F(X) + X
    # F(X) → Konvolüsyon katmanlarından gelen özelliklerdir.
    # X → Shortcut (kısa yol) bağlantısıdır.
    # eğer X ve F(X) aynı boyutta değilde toplama işlemi yapılamaz. Bu nedenle xin boyutunu fxe uygun uygun hale getirmeliyiz.
    # 1️⃣ Eğer stride != 1 ise:
    #   Yani, stride 1'den farklıysa, giriş ile çıkışın boyutu uyuşmaz.
    #    Çözüm: 1x1 konvolüsyon ile shortcut’u yeniden boyutlandırırız.

    # 2️⃣ Eğer shortcut.shape[-1] != filters * 4 ise:
    #   shortcut.shape[-1], giriş verisinin kanal sayısını temsil eder.
    #   filters * 4, çıkış verisinin kanal sayısını temsil eder.
    #   Eğer giriş ve çıkışın kanal sayıları farklıysa, toplama işlemi yapılamaz.
    #   Çözüm: 1x1 konvolüsyon ile girişin kanal sayısını artırırız.

    # **Shortcut (Bağlantı)**
    if stride != 1 or shortcut.shape[-1] != filters * 4:
        shortcut = Conv2D(filters * 4, (1,1), strides=stride, padding='same')(shortcut)
        shortcut = BatchNormalization()(shortcut)

    # kernel_size = (1,1) olduğundan:
    # 1x1 konvolüsyon, her bir pikselin değerini tek tek işleyerek kanal boyutlarını değiştiren özel bir konvolüsyon türüdür.
    # Eğer girişin kanal sayısı, çıkışın kanal sayısından farklıysa, 1x1 konvolüsyon kullanılarak eşitleme yapılır.

    # **Toplama işlemi (F(X) + X)**
    x = Add()([x, shortcut])
    x = Activation('relu')(x)

    return x


# **ResNet-50 Modelini Oluşturma**
def build_resnet50(input_shape=(224, 224, 3), num_classes=1000):
    inputs = Input(shape=input_shape)

    # **Başlangıç Konvolüsyonu**
    x = Conv2D(64, (7,7), strides=2, padding='same')(inputs)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = MaxPooling2D(pool_size=(3,3), strides=2, padding='same')(x)

    # **Residual Bloklar**
    x = residual_block(x, 64, stride=1)
    x = residual_block(x, 64, stride=1)
    x = residual_block(x, 64, stride=1)

    x = residual_block(x, 128, stride=2)
    x = residual_block(x, 128, stride=1)
    x = residual_block(x, 128, stride=1)
    x = residual_block(x, 128, stride=1)

    x = residual_block(x, 256, stride=2)
    x = residual_block(x, 256, stride=1)
    x = residual_block(x, 256, stride=1)
    x = residual_block(x, 256, stride=1)
    x = residual_block(x, 256, stride=1)
    x = residual_block(x, 256, stride=1)

    x = residual_block(x, 512, stride=2)
    x = residual_block(x, 512, stride=1)
    x = residual_block(x, 512, stride=1)

    # **Global Ortalama Havuzlama**
    x = GlobalAveragePooling2D()(x)

    # **Tam Bağlantılı Katman**
    outputs = Dense(num_classes, activation='softmax')(x)

    # **Modeli Tanımla**
    model = Model(inputs, outputs)
    return model

# **ResNet-50 Modelini Başlat**
model = build_resnet50()

# **Modeli Özetle**
model.summary()

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# **Eğitim**
model.fit(x_train, y_train, epochs=10, batch_size=32, validation_data=(x_test, y_test))

test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"Test Doğruluğu: {test_acc:.4f}")


