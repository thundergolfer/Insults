import keras.callbacks
import logging
import re
import tensorflow as tf


def setup_logging(module_name):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)

    return logger


class LossHistory(keras.callbacks.Callback):
    """
    Record history of training
    """
    def on_train_begin(self, logs={}):
        self.losses = []
        self.accuracies = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))
        self.accuracies.append(logs.get('acc'))


def binarize(x, sz=71):
    return tf.to_float(tf.one_hot(x, sz, on_value=1, off_value=0, axis=-1))


def binarize_outshape(in_shape):
    return in_shape[0], in_shape[1], 71


def striphtml(s):
    p = re.compile(r'<.*?>')
    return p.sub('', s)


def clean(s):
    return re.sub(r'[^\x00-\x7f]', r'', s)
