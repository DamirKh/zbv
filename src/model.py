__ver__ = '1.0.1'
import pickle
import logging
from binascii import a2b_base64 as a2b
from binascii import b2a_base64 as b2a
# from keras.layers import Dense
# from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.models import load_model, save_model
from keras.layers import Dense, Input
from keras.models import Model as KerasModel

import h5py  # HDF5 support

from constants import *
from layers_opt import CommonLayerConfig
from loss_and_optim import CommonOptimizerConfig


class Model(object):
    def __init__(self,
                 layers=None,
                 data_conf=None,
                 optimizer=None,
                 loss=None,
                 metrics=['accuracy']):
        # self.optimizer = optimizer
        # self.loss = loss
        # self.metrics = metrics
        # self.data_conf = data_conf
        # self.layers = layers
        self.conf = {
            'ver': __ver__,
            'optimizer': optimizer,
            'loss': loss,
            'metrics': metrics,
            'data_conf': data_conf,
            'layers': layers,
        }

        self.model = Sequential()

        self.ss_saved = False
        self.ss_loaded = False

    @property
    def optimizer(self):
        return self.conf['optimizer']

    @property
    def loss(self):
        return self.conf['loss']

    @property
    def metrics(self):
        return self.conf['metrics']

    @property
    def data_conf(self):
        return self.conf['data_conf']

    @property
    def layers(self):
        return self.conf['layers']

    def compile(self):
        assert self.layers is not None
        assert isinstance(self.optimizer, CommonOptimizerConfig)
        first_layer_flag = True
        for layer_conf in self.layers:
            if layer_conf is None:
                continue
            assert isinstance(layer_conf, CommonLayerConfig)
            print("Add Layer")
            overload_arguments = {}
            if first_layer_flag:
                first_layer_flag = False
                # here we should define the shape of first layer
                # https://keras.io/getting-started/sequential-model-guide/#specifying-the-input-shape
                # input_dim is equal to the numbers of input tags
                input_shape = (self.data_conf[WINDOW_SIZE], self.data_conf[INPUT_TAGS_TOTAL])
                overload_arguments['input_shape'] = input_shape
            keras_layer = layer_conf.get_KERAS_layer(**overload_arguments)

            self.model.add(keras_layer)
            print(self.model)
        optimizer = self.optimizer.get_KERAS_optimizer(clipnorm=1.0)
        self.model.compile(optimizer=optimizer, loss=self.loss, metrics=self.metrics)

    def compile2(self):
        assert self.layers is not None
        assert isinstance(self.optimizer, CommonOptimizerConfig)
        WINDOW_LENGTH = self.data_conf[WINDOW_SIZE]
        DATA_DIM = self.data_conf[INPUT_TAGS_TOTAL]
        input1 = Input(shape=(WINDOW_LENGTH, DATA_DIM))
        first_layer_flag = True
        for layer_conf in self.layers:
            if layer_conf is None:
                continue
            assert isinstance(layer_conf, CommonLayerConfig)
            print("Add Layer")
            overload_arguments = {}
            if first_layer_flag:
                first_layer_flag = False
                keras_layer = layer_conf.get_KERAS_layer(**overload_arguments)(input1)
            else:
                # current layer                                              prevision layer
                keras_layer = layer_conf.get_KERAS_layer(**overload_arguments)(keras_layer)

        self.model = KerasModel(inputs=input1, outputs=keras_layer)
        print(self.model)
        optimizer = self.optimizer.get_KERAS_optimizer(clipvalue=1.0, )
        self.model.compile(optimizer=optimizer, loss=self.loss, metrics=self.metrics)

    def savemodel(self, filename):
        """save model to file"""
        # https://keras.io/getting-started/faq/#how-can-i-save-a-keras-model
        # https://stackoverflow.com/a/49939851/8124158  показано как сохранить любой объект в h5
        logging.debug("saving model to '%s'" % filename)
        try:
            self.model.save(filename)
            logging.info("Model train data file '%s' saved" % filename)
        except AttributeError:
            logging.error('Model was not initialised properly!')
            return False
        f = h5py.File(filename, 'r+')
        # print(b2a(pickle.dumps(self.conf)))
        f.attrs['zbv_meta'] = b2a(pickle.dumps(self.conf))
        logging.debug('Model meta info saved')
        f.close()
        self.ss_saved = True
        return True

    def loadmodel(self, filename):
        """Load model from file"""
        logging.debug('loading model from <%s>' % filename)
        try:
            self.model = load_model(filename)
            logging.info("KERAS Model loaded from <%s>" % filename)
        except AttributeError:
            logging.error("Error while loading KERAS model from <%s>" % filename)
            return False
        with h5py.File(filename, 'r') as f:
            try:
                self.conf = pickle.loads(a2b(f.attrs['zbv_meta']))
                logging.info("ZBV Model configuration <%s> loaded" % f.name)
            except AttributeError:
                logging.error('Error while loading ZBV model from <%s>' % f.name)
                return False
        self.ss_loaded = True
        self.ss_saved = False
        return True
