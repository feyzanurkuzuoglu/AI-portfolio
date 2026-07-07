import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
# tf.config.experimental.set_memory_growth(physical_devices[0], True)




# initialization of tensors
x = tf.constant(4, shape=(1,1), dtype=tf.float32)
x = tf.constant([[1,2,3], [4,5,6]])
x = tf.ones((3,3))
x = tf.zeros((3,2))
x = tf.eye(4) # I for identity matrix (eye=I)
x = tf.random.normal((3,3), mean=0, stddev=1)  #standart normal deviation
x = tf.random.uniform((1,3), minval=0, maxval=1)
x = tf.range(10)
x = tf.range(start=1, limit=10, delta=3, dtype=tf.int32) #delta = step
x = tf.cast(x, dtype=tf.float32) #converting type, tf.float, tf.int, tf.bool

# mathematical operations

x = tf.constant([1,2,3])
y = tf.constant([9,8,7])
    #  element wise
z = tf.add(x,y)
z = x + y
z = tf.subtract(x,y)
z = x - y
z = tf.divide(x,y)
z = x/y
z = tf.multiply(x,y)
z = x*y
z = x**2

    #dot product
z = tf.tensordot(x,y,axes=1)
z = tf.reduce_sum(x*y,0)

    # matrix multiplication
x = tf.random.normal((2,3))
y = tf.random.normal((3,4))
z = tf.matmul(x,y)
z = x @ y

# indexing
x = tf.constant([1,2,3,4,5,6,7,8,9])
# print(x[1:3])
# print(x[::2])
indices = tf.constant([0,3,4])
x_ind = tf.gather(x,indices) #bu indislerdeki değerleri al

x = tf.constant([[1,2],
                [3,4],
                [5,6]])
# print(x[0])
# print(x[0,:])
# print(x[0:2])
# print(x[0:2,:])
# print(x[0:2,0:2])


# reshaping
x = tf.range(9)
x = tf.reshape(x, (3,3))
print(x)
x = tf.transpose(x, perm=[1,0])  # perm default olarak bu değerde oluyor
# x = tf.transpose(x, perm=[1,0])
print(x)











