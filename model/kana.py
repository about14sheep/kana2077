import tensorflow as tf

import numpy as np
import matplotlib as plt
import tensorflow_datasets as tfds

print(tf.__version__)

(ds_train, ds_test), ds_info = tfds.load(
    'kmnist', split=['train', 'test'], shuffle_files=True, as_supervised=True, with_info=True)


def normalize_img(image, label):
    return tf.cast(image, tf.float32) / 255., label


ds_train = ds_train.map(
    normalize_img, num_parallel_calls=tf.data.experimental.AUTOTUNE)
ds_train = ds_train.cache()
ds_train = ds_train.shuffle(ds_info.splits['train'].num_examples)
ds_train = ds_train.batch(128)
ds_train = ds_train.prefetch(tf.data.experimental.AUTOTUNE)


ds_test = ds_test.map(
    normalize_img, num_parallel_calls=tf.data.experimental.AUTOTUNE)
ds_test = ds_test.batch(128)
ds_test = ds_test.cache()
ds_test = ds_test.prefetch(tf.data.experimental.AUTOTUNE)

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10)
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
)

model.fit(
    ds_train,
    epochs=6,
    validation_data=ds_test,
)


prob_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])


test_num = 3
test = ds_test.take(1)


for image, label in test:
    print(image.shape, label[test_num])


predict_single = prob_model.predict(image)
print(np.argmax(predict_single[test_num]))
