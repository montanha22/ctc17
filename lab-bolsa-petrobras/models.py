import tensorflow as tf

def model1()->tf.keras.Model:
    input_layer = tf.keras.layers.Input(shape = (10))
    hidden_layer = tf.keras.layers.Dense(units = 15, activation = 'tanh')(input_layer)
    output_layer = tf.keras.layers.Dense(units = 1, activation = 'linear')(hidden_layer)
    model = tf.keras.Model(inputs = input_layer, outputs = output_layer)
    return model

def model2()->tf.keras.Model:
    input_layer = tf.keras.layers.Input(shape = (10))
    hidden_layer = tf.keras.layers.Dense(units = 10, activation = 'relu')(input_layer)
    hidden_layer = tf.keras.layers.Dense(units = 10, activation = 'relu')(hidden_layer)
    output_layer = tf.keras.layers.Dense(units = 1, activation = 'linear')(hidden_layer)
    model = tf.keras.Model(inputs = input_layer, outputs = output_layer)
    return model

def model3()->tf.keras.Model:
    input_layer = tf.keras.layers.Input(shape = (10))
    hidden_layer = tf.keras.layers.Dense(units = 15, activation = 'sigmoid')(input_layer)
    hidden_layer = tf.keras.layers.Dense(units = 15, activation = 'relu')(hidden_layer)
    output_layer = tf.keras.layers.Dense(units = 1, activation = 'linear')(hidden_layer)
    model = tf.keras.Model(inputs = input_layer, outputs = output_layer)
    return model

def model4()->tf.keras.Model:
    input_layer = tf.keras.layers.Input(shape = (10))
    hidden_layer = tf.keras.layers.Dense(units = 25, activation = 'relu')(input_layer)
    output_layer = tf.keras.layers.Dense(units = 10, activation = 'linear')(hidden_layer)
    model = tf.keras.Model(inputs = input_layer, outputs = output_layer)
    return model

def model5()->tf.keras.Model:
    input_layer = tf.keras.layers.Input(shape = (6))
    hidden_layer = tf.keras.layers.Dense(units = 25, activation = 'tanh')(input_layer)
    hidden_layer = tf.keras.layers.Dense(units = 25, activation = 'tanh')(hidden_layer)
    output_layer = tf.keras.layers.Dense(units = 2, activation = 'linear')(hidden_layer)
    model = tf.keras.Model(inputs = input_layer, outputs = output_layer)
    return model

def model6()->tf.keras.Model:
    input_layer = tf.keras.layers.Input(shape = (8))
    hidden_layer = tf.keras.layers.Dense(units = 16, activation = 'sigmoid')(input_layer)
    hidden_layer = tf.keras.layers.Dense(units = 16, activation = 'tanh')(hidden_layer)
    output_layer = tf.keras.layers.Dense(units = 2, activation = 'linear')(hidden_layer)
    model = tf.keras.Model(inputs = input_layer, outputs = output_layer)
    return model