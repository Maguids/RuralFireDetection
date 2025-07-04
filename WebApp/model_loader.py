from tensorflow.keras.models import Model
from tensorflow.keras.layers import (Input, Conv2D, DepthwiseConv2D, GlobalAveragePooling2D, GlobalMaxPooling2D, Dense, ReLU,
                                     BatchNormalization, MaxPooling2D, Dropout, AveragePooling2D, Concatenate,
                                     Flatten, LayerNormalization, Multiply, Add, Activation, Reshape, Lambda)
from tensorflow.keras import backend as K
import tensorflow as tf


def build_model_1(input_shape=(224, 224, 3), num_classes=2):
    inputs = Input(shape=input_shape)
    x = Conv2D(48, (3, 3), strides=2, padding='same')(inputs)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    x = DepthwiseConv2D(kernel_size=3, strides=1, padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    x = Conv2D(24, (1, 1), padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    x = Conv2D(72, (1, 1), padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    x = DepthwiseConv2D(kernel_size=3, strides=2, padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    x = Conv2D(24, (1, 1), padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    for _ in range(2):
        x = Conv2D(72, (1, 1), padding='same')(x)
        x = BatchNormalization()(x)
        x = ReLU()(x)
        x = DepthwiseConv2D(kernel_size=3, padding='same')(x)
        x = BatchNormalization()(x)
        x = ReLU()(x)
        x = Conv2D(24, (1, 1), padding='same')(x)
        x = BatchNormalization()(x)
        x = ReLU()(x)

    x = Conv2D(72, (1, 1), padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    x = DepthwiseConv2D(kernel_size=5, strides=2, padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    x = Conv2D(56, (1, 1), padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    for _ in range(2):
        x = Conv2D(168, (1, 1), padding='same')(x)
        x = BatchNormalization()(x)
        x = ReLU()(x)
        x = DepthwiseConv2D(kernel_size=5, padding='same')(x)
        x = BatchNormalization()(x)
        x = ReLU()(x)
        x = Conv2D(56, (1, 1), padding='same')(x)
        x = BatchNormalization()(x)
        x = ReLU()(x)

    x = Conv2D(336, (1, 1), padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    x = DepthwiseConv2D(kernel_size=5, strides=2, padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    x = Conv2D(104, (1, 1), padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    for _ in range(2):
        x = Conv2D(624, (1, 1), padding='same')(x)
        x = BatchNormalization()(x)
        x = ReLU()(x)
        x = DepthwiseConv2D(kernel_size=5, padding='same')(x)
        x = BatchNormalization()(x)
        x = ReLU()(x)
        x = Conv2D(104, (1, 1), padding='same')(x)
        x = BatchNormalization()(x)
        x = ReLU()(x)

    x = Conv2D(624, (1, 1), padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    x = DepthwiseConv2D(kernel_size=3, padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    x = Conv2D(136, (1, 1), padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    x = Conv2D(816, (1, 1), padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    x = DepthwiseConv2D(kernel_size=3, padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    x = Conv2D(136, (1, 1), padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    x = Conv2D(816, (1, 1), padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    x = DepthwiseConv2D(kernel_size=5, strides=2, padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    x = Conv2D(272, (1, 1), padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    for _ in range(3):
        x = Conv2D(1632, (1, 1), padding='same')(x)
        x = BatchNormalization()(x)
        x = ReLU()(x)
        x = DepthwiseConv2D(kernel_size=5, padding='same')(x)
        x = BatchNormalization()(x)
        x = ReLU()(x)
        x = Conv2D(272, (1, 1), padding='same')(x)
        x = BatchNormalization()(x)
        x = ReLU()(x)

    x = Conv2D(1632, (1, 1), padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    x = DepthwiseConv2D(kernel_size=3, padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    x = Conv2D(448, (1, 1), padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    x = Conv2D(1280, (1, 1), padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    x = GlobalAveragePooling2D()(x)
    outputs = Dense(num_classes, activation='softmax')(x)

    return Model(inputs=inputs, outputs=outputs)


def channel_attention(input_feature, reduction_ratio=8):
    channel = input_feature.shape[-1]
    shared_dense_one = Dense(channel // reduction_ratio, activation='relu', kernel_initializer='glorot_uniform')
    shared_dense_two = Dense(channel, activation='relu', kernel_initializer='glorot_uniform')
    avg_pool = GlobalAveragePooling2D()(input_feature)
    max_pool = GlobalMaxPooling2D()(input_feature)
    avg_out = shared_dense_two(shared_dense_one(avg_pool))
    max_out = shared_dense_two(shared_dense_one(max_pool))
    cbam_feature = Add()([avg_out, max_out])
    cbam_feature = Activation('relu')(cbam_feature)
    cbam_feature = Reshape((1, 1, channel))(cbam_feature)
    return Multiply()([input_feature, cbam_feature])

class MeanLayer(tf.keras.layers.Layer):
    def call(self, inputs):
        return tf.reduce_mean(inputs, axis=-1, keepdims=True)

class MaxLayer(tf.keras.layers.Layer):
    def call(self, inputs):
        return tf.reduce_max(inputs, axis=-1, keepdims=True)

def spatial_attention(input_feature):
    avg_pool = MeanLayer()(input_feature)
    max_pool = MaxLayer()(input_feature)
    concat = Concatenate(axis=-1)([avg_pool, max_pool])
    concat = LayerNormalization()(concat)
    conv = Conv2D(1, kernel_size=7, padding='same', activation='relu')(concat)
    gate = Conv2D(1, kernel_size=1, padding='same', activation='sigmoid')(concat)
    gated = Multiply()([conv, gate])
    return Multiply()([input_feature, gated])

def AHC_block(input_tensor):
    conv_3x3 = Conv2D(32, kernel_size=3, padding='same', activation='relu')(input_tensor)
    conv_5x5 = Conv2D(32, kernel_size=5, padding='same', activation='relu')(input_tensor)
    conv_7x7 = Conv2D(32, kernel_size=7, padding='same', activation='relu')(input_tensor)
    pool_3x3 = AveragePooling2D(pool_size=2, strides=1, padding='same')(conv_3x3)
    pool_5x5 = AveragePooling2D(pool_size=2, strides=1, padding='same')(conv_5x5)
    pool_7x7 = AveragePooling2D(pool_size=2, strides=1, padding='same')(conv_7x7)
    return Concatenate()([pool_3x3, pool_5x5, pool_7x7])

def build_AHMHCNN_mCBAM(input_shape=(256, 256, 3), num_classes=2):
    inputs = Input(shape=input_shape)
    x = Conv2D(32, kernel_size=3, padding='same', activation='relu')(inputs)
    x = MaxPooling2D(pool_size=2)(x)
    x = Conv2D(48, kernel_size=3, padding='same', activation='relu')(x)
    x = MaxPooling2D(pool_size=2)(x)
    x = Conv2D(64, kernel_size=5, padding='same', activation='relu')(x)
    x = MaxPooling2D(pool_size=2)(x)
    x = Dropout(0.02)(x)
    x = Conv2D(32, kernel_size=3, padding='same', activation='relu')(x)
    x = MaxPooling2D(pool_size=2)(x)
    x = BatchNormalization()(x)
    x = Dropout(0.02)(x)
    x = AHC_block(x)
    x = channel_attention(x)
    x = spatial_attention(x)
    x = Flatten()(x)
    x = Dense(56, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dense(48, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dense(32, activation='relu')(x)
    x = BatchNormalization()(x)
    outputs = Dense(num_classes, activation='softmax')(x)
    return Model(inputs=inputs, outputs=outputs)