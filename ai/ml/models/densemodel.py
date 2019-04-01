import tensorflow as tf

def newDenseModel(inputsize, layer_sizes, init_lr, lr_decay):
    """
    Function returning a basic NN with the following layers:
    """
    model = tf.keras.models.Sequential()

    model.add(tf.keras.layers.Dense(layer_sizes[0], input_dim=inputsize))

    for layersize in layer_sizes[1:]:
        model.add(tf.keras.layers.Dense(layersize, activation=tf.nn.relu))

    model.add(tf.keras.layers.Dense(1))
    model.add(tf.keras.layers.LeakyReLU(alpha=0.3))
    opt = tf.keras.optimizers.Adam(lr=init_lr, decay=lr_decay)
    model.compile(loss='mse', optimizer=opt)

    return model
    