import tensorflow as tf

def newDenseModel(inputsize, layer_sizes):
    """
    Function returning a basic NN with the following layers:
    """
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Input(shape=(inputsize,), dtype = tf.float32))

    for _ in range(0, hiddenlayers):
        model.add(tf.keras.layers.Dense(64, activation=tf.nn.relu))


    return model
    