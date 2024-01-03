import tensorflow as tf
from tensorflow.python import keras
from keras.models import Model
from keras.layers import Conv2D, AveragePooling2D, Input, Concatenate, Flatten, Dense


def fractal_block(x, filter):
    conv = Conv2D(filter, kernel_size=(3, 3), activation='relu', padding='same')(x)
    union = Concatenate()([x, conv])

    return union


def fractal_network(input_shape, width, depth, drop_prob):
    inputs = Input(shape=input_shape)

    x = Conv2D(width, kernel_size=(3, 3), activation='relu', padding='same')(inputs)

    for _ in range(depth):
        x = fractal_block(x, width)

    flattened_output = Flatten()(x)
    output_layer = Dense(1, activation='sigmoid')(flattened_output)

    model = Model(inputs, output_layer)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model


input_shape = (256, 256, 3)
fractal_model = fractal_network(input_shape, width=32, depth=3, drop_prob=0.2)
fractal_model.summary()
