import tensorflow as tf
from tensorflow.python import keras
from keras.models import Model
from keras.layers import Conv2D, AveragePooling2D, Input, Concatenate, Flatten, Dense, BatchNormalization, LeakyReLU, \
    MaxPooling2D, Dropout


class ConvBlock(Model):
    def __init__(self, filters, kernel_size, padding):
        super().__init__()
        self.conv = Conv2D(filters, kernel_size=kernel_size, padding=padding)
        self.bn = BatchNormalization()
        self.relu = LeakyReLU(alpha=0.01)

    def call(self, inputs, training=None, mask=None):
        x = self.conv(inputs)
        x = self.bn(x)
        x = self.relu(x)
        return x


class FractalBlock(Model):
    def __init__(self, C, filters, kernel_size, padding):
        super().__init__()
        self.columns_count = C
        self.conv_block = ConvBlock(filters, kernel_size, padding)

    def join(self, first_input, second_input):
        return (first_input + second_input) / 2

    def call(self, inputs, training=None, mask=None):
        fc = self.conv_block(inputs)

        for _ in range(self.columns_count - 1):
            fc = self.conv_block(fc)
            fc = self.join(inputs, fc)

        return fc


class FractalNetwork(Model):
    def __init__(self, input_shape, depth, C, filters, kernel_size, padding, drop_prob):
        super().__init__()
        self.depth = depth
        self.columns_count = C
        self.filters = filters
        self.kernel_size = kernel_size
        self.padding = padding
        self.drop_prob = drop_prob

        self.inputs = Input(shape=input_shape)
        self.fractal_blocks = [FractalBlock(self.columns_count, self.filters, self.kernel_size, self.padding)
                               for _ in range(self.depth)]
        self.pooling_layers = [MaxPooling2D(pool_size=(2, 2), strides=None, padding='same')
                               for _ in range(self.depth)]
        self.dropout_layer = Dropout(self.drop_prob, input_shape=(2,))

        self.flatten = Flatten()
        self.dense = Dense(1, activation='sigmoid')

    def call(self, inputs, training=None, mask=None):
        x = inputs
        for i in range(self.depth):
            x = self.fractal_blocks[i](x)
            x = self.pooling_layers[i](x)
            x = self.dropout_layer(x)

        x = self.flatten(x)
        output_layer = self.dense(x)
        return output_layer


shape = (256, 256, 3)
fractal_model = FractalNetwork(shape, depth=3, C=2, filters=32, kernel_size=(3, 3), padding='same', drop_prob=0.2)

fractal_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

fractal_model.summary()
