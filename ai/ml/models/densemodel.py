import tensorflow as tf

def newDenseModel(inputsize, layer_sizes):
    """
    Function returning a basic NN with the following layers:
    """
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Input(shape=(inputsize,), dtype = tf.float32))

    for layersize in layer_sizes:
        model.add(tf.keras.layers.Dense(layersize, activation=tf.nn.relu))

    return model
    