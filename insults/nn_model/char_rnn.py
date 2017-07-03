from keras.models import Model
from keras.layers import Dense, Input, Dropout, MaxPooling1D, Conv1D
from keras.layers import LSTM, Lambda
from keras.layers import TimeDistributed, Bidirectional
import numpy as np
import keras.callbacks
import sys
import os

from insults.util import data_file
from insults.nn_model.util import setup_logging, LossHistory, binarize, binarize_outshape
from insults.nn_model.plumbing import load_data, load_insults_data, build_examples_with_their_targets
from insults.nn_model.plumbing import sentence_count_per_doc, charset, chars_to_indices_vec
from insults.nn_model.plumbing import shuffle_dataset, dataset_split, strip_quotes

logger = setup_logging(__name__)

INSULTS_TRAIN_DATA_FILE = data_file('Inputs','train.csv')
INSULTS_TEST_DATA_FILE = data_file('Inputs','test_with_solutions.csv')

total = len(sys.argv)
cmdargs = str(sys.argv)

logger.info("Script name: %s" % str(sys.argv[0]))

insults_data = load_insults_data(INSULTS_TRAIN_DATA_FILE, INSULTS_TEST_DATA_FILE)

comments, targets = build_examples_with_their_targets(insults_data.Comment, insults_data.Insult)
comments = strip_quotes(comments)

num_sent = sentence_count_per_doc(comments)
chars = charset(comments)

logger.info('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

logger.info('Sample comment {}'.format(comments[len(comments)//2]))

maxlen = 512
max_sentences = 15

X = chars_to_indices_vec(comments, char_indices, max_sentences, maxlen)
y = np.array(targets)

logger.info('Sample chars in X:{}'.format(X[1200, 2]))
logger.info('y:{}'.format(y[1200]))

X, y = shuffle_dataset(X, y)
X_train, X_test, y_train, y_test = dataset_split(X, y, train_end=20000, test_start=20000)

filter_length = [5, 3, 3]
nb_filter = [196, 196, 256]
pool_length = 2
# document input
document = Input(shape=(max_sentences, maxlen), dtype='int64')
# sentence input
in_sentence = Input(shape=(maxlen,), dtype='int64')
# char indices to one hot matrix, 1D sequence to 2D
embedded = Lambda(binarize, output_shape=binarize_outshape)(in_sentence)
# embedded: encodes sentence
for i in range(len(nb_filter)):
    embedded = Conv1D(filters=nb_filter[i],
                      kernel_size=filter_length[i],
                      padding='valid',
                      activation='relu',
                      kernel_initializer='glorot_normal',
                      strides=1)(embedded)

    embedded = Dropout(0.1)(embedded)
    embedded = MaxPooling1D(pool_size=pool_length)(embedded)

bi_lstm_sent = Bidirectional(
                             LSTM(
                                  128,
                                  return_sequences=False,
                                  dropout=0.15,
                                  recurrent_dropout=0.15,
                                  implementation=0
                                 )
                            )(embedded)

sent_encode = Dropout(0.3)(bi_lstm_sent)

encoder = Model(inputs=in_sentence, outputs=sent_encode)  # sentence encoder
encoder.summary()

encoded = TimeDistributed(encoder)(document)

# encoded: sentences to bi-lstm for document encoding
b_lstm_doc = Bidirectional(
                           LSTM(
                                128,
                                return_sequences=False,
                                dropout=0.15,
                                recurrent_dropout=0.15,
                                implementation=0)
                          )(encoded)

output = Dropout(0.3)(b_lstm_doc)
output = Dense(128, activation='relu')(output)
output = Dropout(0.3)(output)
output = Dense(1, activation='sigmoid')(output)

model = Model(inputs=document, outputs=output)

model.summary()

checkpoint = None
if len(sys.argv) == 2:
    if os.path.exists(str(sys.argv[1])):
        print ("Checkpoint : %s" % str(sys.argv[1]))
        checkpoint = str(sys.argv[1])

if checkpoint:
    model.load_weights(checkpoint)

file_name = os.path.basename(sys.argv[0]).split('.')[0]
checkpoint_location = 'checkpoints/' + file_name + '.{epoch:02d}-{val_loss:.2f}.hdf5'

check_cb = keras.callbacks.ModelCheckpoint(checkpoint_location,
                                           monitor='val_loss',
                                           verbose=0, save_best_only=True, mode='min')

earlystop_cb = keras.callbacks.EarlyStopping(
                                             monitor='val_loss',
                                             patience=7,
                                             verbose=1,
                                             mode='auto'
                                            )
history = LossHistory()
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X_train, y_train, validation_data=(X_test, y_test), batch_size=10,
          epochs=5, shuffle=True, callbacks=[earlystop_cb, check_cb, history])

# just showing access to the history object
logger.info(history.losses)
logger.info(history.accuracies)
