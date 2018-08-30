import datetime
from collections import OrderedDict

from keras.layers import Dense, MaxPool1D, SimpleRNN, GRU
from keras.layers.recurrent import LSTM
from keras.models import load_model
from keras.optimizers import SGD
from MyExceptions import NotDefinedError

# ========================
UNITS = 'units'
ACTIVATION = 'activation'
RECURRENT_ACTIVATION = 'recurrent_activation'
USE_BIAS = 'use_bias'
KERNEL_INITIALIZER = 'kernel_initializer'
# ========================


class CommonProp(object):
    def __bool__(self):
        """True if property was configured.
        False if property was not configured"""
        return self.configured

    def drop(self):
        """Drops configured state"""
        self.configured = False


class BoolProp(CommonProp):
    def __init__(self, description='Some boolean object', www=None, state=None, help_=None):
        self.help = description if (help_ is None) else help_
        self.www = 'https://www.google.com/search?q=%s' % help_ if (www is None) else www
        self.__doc__ = description
        if state is None:
            self.configured = False
        else:
            self.configured = True
            self.__state = state

    def __call__(self, state=None):
        if state is not None:
            self.configured = True
            self.__state = state
            return self.__state
        else:
            if self.configured:
                return self.__state
            else:
                raise NotDefinedError


class SelectOneProp(CommonProp):
    #           key <---vv   +----------+---> value   pair of  __rawsetofchoice dict
    # __setofchoice <---vv   v          v     elements of __setofchoice list
    default_choice = ['first First choice',
                      'second Second choice',
                      'last Last choice']

    def __init__(self, setofchoice=default_choice, description='Make Your choice', www=r'https://www.google.com/',
                 choice=None, ):
        self.__doc__ = description
        self.www = www
        # i=''
        self.__setofchoice = [i.split(' ', 2)[0] for i in setofchoice]
        self.__rawsetofchoice = {i.split(' ', 1)[0]: i.split(' ', 1)[-1] for i in setofchoice}
        # print(self.__rawsetofchoice)
        if choice is None:
            self.configured = False
        else:
            self.configured = True
            self.__choice = choice

    def __call__(self, choice=None):
        """If call with no choice return current choice if configured or raise NotDefinedError if not configured.
        If call with choice configure new choice"""
        if choice is not None:
            # set new choice
            self.configured = True
            if choice not in self.__setofchoice:
                self.__setofchoice.append(choice)
            self.__choice = choice
        elif not self.configured:
            # getting choice but choice is not configured yet
            raise NotDefinedError
        # print('SelectOneProp:', self.__choice, self.__rawsetofchoice[self.__choice])
        return self.__choice

    def __iter__(self):
        # https://stackoverflow.com/a/4020011/8124158
        return self.__setofchoice.__iter__()

    def __len__(self):
        return len(self.__setofchoice)

    def __contains__(self, item):
        return item in self.__setofchoice


class IntRangeProp(CommonProp):
    def __init__(self, rng=(0, 100), description=None, www=r'https://www.google.com/', value=None):
        self.www = www
        if description is None:
            self.__doc__ = 'Range of integers %i .. %i' % rng
        else:
            self.__doc__ = description
        if rng[0] < rng[1]:
            self.__min, self.__max = rng
        else:
            raise ValueError
        if value is None:
            self.configured = False
        else:
            self.configured = True
            self.__value = value

    @property
    def min(self):
        """Range minimum"""
        return self.__min

    @property
    def max(self):
        """Range maximum"""
        return self.__max

    def __call__(self, value=None):
        if value is not None:
            # set new value
            value = int(value)
            if self.__min <= value <= self.__max:
                self.configured = True
                self.__value = value
            else:
                raise ValueError
        elif not self.configured:
            # getting choice but choice is not configured yet
            raise NotDefinedError
        # print(self.__doc__, '=', self.__value)
        return self.__value


class RealRangeProp(IntRangeProp):
    def __init__(self, rng=(0., 1.), description=None, www=r'https://www.google.com/', value=None):
        self.www = www
        if description is None:
            self.__doc__ = 'Range of real %i .. %i' % rng
        else:
            self.__doc__ = description
        if rng[0] < rng[1]:
            self.__min, self.__max = rng
        else:
            raise ValueError
        if value is None:
            self.configured = False
        else:
            self.configured = True
            self.__value = value

    def __call__(self, value=None):
        if value is not None:
            # set new value
            value = float(value)
            if self.__min <= value <= self.__max:
                self.configured = True
                self.__value = value
            else:
                raise ValueError
        elif not self.configured:
            # getting choice but choice is not configured yet
            raise NotDefinedError
        return self.__value


# https://keras.io/activations/
avail_act = ['softmax Softmax activation function',
             'elu See documentation',
             'selu Scaled Exponential Linear Unit.',
             'softplus See documentation',
             'softsign See documentation',
             'relu See documentation',
             'tanh See documentation',
             'sigmoid See documentation',
             'hard_sigmoid See documentation',
             'linear See documentation',
             ]

# https://keras.io/initializers/
# some initializers was skipped
avail_initializer = ['zeros Initializer that generates tensors initialized to 0',
                     'ones Initializer that generates tensors initialized to 1',
                     'constant Initializer that generates tensors initialized to a constant value',
                     'normal Initializer that generates tensors with a normal distribution',
                     'uniform Initializer that generates tensors with a uniform distribution',
                     'truncated Initializer that generates a truncated normal distribution',
                     'orthogonal Initializer that generates a random orthogonal matrix',
                     'identity Initializer that generates the identity matrix',
                     'lecun_uniform LeCun uniform initializer',
                     'glorot_normal Glorot normal initializer, also called Xavier normal initializer',
                     'glorot_uniform Glorot uniform initializer, also called Xavier uniform initializer',
                     'he_normal He normal initializer',
                     'lecun_normal LeCun normal initializer',
                     'he_uniform He uniform variance scaling initializer',
                     ]


def layer_activation_any(choice=None):
    """ activation type Helper.
    Return SelectOneProp configured for use with all available activation"""
    return SelectOneProp(avail_act, description='Layer activation function',
                         www=r'https://keras.io/activations/',
                         choice=choice)


def num_of_units_any(max_=500, www=None, **kwargs):
    """Dimensionality of the output space helper.
    Returns IntRangeProp configured for use as Dimensionality of the output space"""
    if www is None:
        www=r'https://keras.io/getting-started/sequential-model-guide/#getting-started-with-the-keras-sequential-model'
    return IntRangeProp((1, max_), "Dimensionality of the output space",
                        www=www,
                        value=kwargs.setdefault('value', 3))


def use_bias_any(state=None):
    """Use bias conf helper
    :returns BoolProp suitable for all layer with bias"""
    if state is None:
        return BoolProp(description="Boolean, whether the layer uses a bias vector",\
                    www=r"https://stackoverflow.com/questions/2480650/role-of-bias-in-neural-networks",)
    else:
        return BoolProp(description="Boolean, whether the layer uses a bias vector", \
                        www=r"https://stackoverflow.com/questions/2480650/role-of-bias-in-neural-networks",
                        state=state)


def initializer_any(choice=None, initializer_of=''):
    """initializer helper
    :returns SelectOneProp configured for use for available initializers"""
    return SelectOneProp(avail_initializer,
                         description="%s Initializer"%initializer_of,
                         www=r"https://keras.io/initializers/",
                         choice=choice)


class CommonLayerConfig(object):
    def __init__(self, name="Strange layer (if You see it - that's an application error)", config_dict=OrderedDict()):
        self.config_dict = config_dict
        self.name = name
        self.touch()
        pass

    def touch(self):
        self.touch_time = datetime.datetime.now()

    def keys(self):
        return self.config_dict.keys()

    def __getitem__(self, key):
        return self.config_dict[key]

    def __setitem__(self, key, item):
        self.__dict__[key](item)
        self.touch()

    def __repr__(self):
        return repr(self.config_dict)

    def __len__(self):
        return len(self.config_dict)

    def __delitem__(self, key):
        del self.config_dict[key]
        self.touch()

    def get_config_as_dict(self):
        d = {}
        for key in self.config_dict.keys():
            d[key] = self.config_dict[key]()
        return d

    def get_KERAS_layer(self, **overload):
        d = dict(self.get_config_as_dict())
        print('='*40)
        d.update(overload)
        print(d)
        print('='*40)
        Layer = self.create_layer_instance(**d)
        return Layer

    def create_layer_instance(self, **d):
        """You should override this method"""
        raise NotImplemented


class DenseLayerConfig(CommonLayerConfig):
    '''Dense https://keras.io/layers/core/#dense'''
    def __init__(self, number=None, **kwargs):
        self.www = r"https://keras.io/layers/core/#dense"
        config = OrderedDict([
            (UNITS, num_of_units_any(**kwargs)),
            (ACTIVATION, layer_activation_any(choice='relu')),
            (USE_BIAS , use_bias_any(True)),
            (KERNEL_INITIALIZER, initializer_any(choice='glorot_uniform', initializer_of="Kernel's"))
        ])
        number = '' if (number is None) else ' #%i'%number
        super().__init__(name='Dense Layer%s'%number, config_dict=config)

    def create_layer_instance(self, **d):
            return Dense(**d)


class MaxPooling1DConfig(CommonLayerConfig):
    '''MaxPooling1D https://keras.io/layers/pooling/#maxpooling1d'''
    def __init__(self, number=None, **kwargs):
        self.www = r'https://keras.io/layers/pooling/#maxpooling1d'
        # http://adventuresinmachinelearning.com/convolutional-neural-networks-tutorial-tensorflow/
        config = OrderedDict([
            ('pool_size', IntRangeProp(rng=(2,100), description='Integer, size of the max pooling windows', value=2)),
            ('padding', SelectOneProp(setofchoice=["valid", "same"], description='One of "valid" or "same"', choice='valid'))
        ])

        number = '' if (number is None) else ' #%i' % number
        super().__init__(name='MaxPooling1D Layer%s' % number, config_dict=config)

    def create_layer_instance(self, **d):
        return MaxPool1D(**d)


class SimpleRNNConfig(CommonLayerConfig):
    '''SimpleRNN https://keras.io/layers/recurrent/#simplernn'''
    def __init__(self, number=None, **kwargs):
        self.www = r'https://keras.io/layers/recurrent/#simplernn'
        config = OrderedDict([
            (UNITS, num_of_units_any()),
            (ACTIVATION, layer_activation_any('tanh')),
            (USE_BIAS, use_bias_any(True)),
            ('stateful', BoolProp(description='If True, the last state for each sample at index i in a batch will be used as initial state for the sample of index i in the following batch',
                                  state=False)),
        ])

        number = '' if (number is None) else ' #%i'%number
        super().__init__(name='SimpleRNN%s'%number, config_dict=config)

    def create_layer_instance(self, **d):
        return SimpleRNN(**d)


class GRUConfig(CommonLayerConfig):
    '''GRU https://keras.io/layers/recurrent/#gru'''
    def __init__(self, number=None, **kwargs):
        self.www = r'https://keras.io/layers/recurrent/#gru'
        # http://www.jackdermody.net/brightwire/article/GRU_Recurrent_Neural_Networks
        config = OrderedDict([
            (UNITS, num_of_units_any(**kwargs)),
            (ACTIVATION, layer_activation_any('tanh')),
            (RECURRENT_ACTIVATION, layer_activation_any('hard_sigmoid')),
            (USE_BIAS, use_bias_any(True)),
            ('return_sequences', BoolProp(description='Whether to return the last output in the output sequence, or the full sequence',
                                          state=False)),
        ])

        number = '' if (number is None) else ' #%i' % number
        super().__init__(name='Gated Recurrent Units Layer%s' % number, config_dict=config)

    def create_layer_instance(self, **d):
        return GRU(**d)


class LSTMConfig(CommonLayerConfig):
    """LSTM https://keras.io/layers/recurrent/#lstm"""
    def __init__(self, number=None, **kwargs):
        self.www = r'https://keras.io/layers/recurrent/#lstm'
        config = OrderedDict([
            (UNITS, num_of_units_any(www=r'https://www.quora.com/In-LSTM-how-do-you-figure-out-what-size-the-weights-are-supposed-to-be', **kwargs)),
            (ACTIVATION, layer_activation_any('tanh')),
            (RECURRENT_ACTIVATION, layer_activation_any('hard_sigmoid')),
            (USE_BIAS, use_bias_any(True)),
            ('return_sequences', BoolProp(description='Whether to return the last output in the output sequence, or the full sequence',
                                          state=False,
                                          www=r'https://machinelearningmastery.com/return-sequences-and-return-states-for-lstms-in-keras/')),
        ])
        number = '' if (number is None) else ' #%i' % number
        super().__init__(name='Long Short-Term Memory layer%s' % number, config_dict=config)

    def create_layer_instance(self, **d):
        return LSTM(**d)


DEFINED_LAYERS = [DenseLayerConfig,
                  MaxPooling1DConfig,
                  SimpleRNNConfig,
                  GRUConfig,
                  LSTMConfig]

if __name__ == '__main__':
    b = BoolProp("Boolean property", )
    print(b)
    if b:
        print("b was configured")
        print('b %s', b())
    else:
        print('b was not configured')

    b(True)
    if b:
        print("b was configured")
        print('b =', b())
    else:
        print('b was not configured')

    b(False)
    if b:
        print("b was configured")
        print('b =', b())
    else:
        print('b was not configured')

    L = SelectOneProp(['a', 'b', 'c', 'd'], "abcd property", )
    if L:
        print('L configured (%s)' % L.__doc__)
        print(L())
    else:
        print('L NOT configured')

    L('b')
    if L:
        print('L configured (%s)' % L.__doc__)
        print(L())
    else:
        print('L NOT configured')

    L('X')
    if L:
        print('L configured (%s)' % L.__doc__)
        print(L())
    else:
        print('L NOT configured')
    [print(x) for x in L]
    print('X' in L)
    print('Y' in L)

    I = IntRangeProp()
    if I:
        print("I configured (%s)" % I.__doc__)
        print(L())
    else:
        print("I not configured")
    I(10)
    if I:
        print("I configured (%s)" % I.__doc__)
        print(I())
    else:
        print("I not configured")

    assert isinstance(I, IntRangeProp)
    assert isinstance(I, BoolProp), "Not a boolean property"
    assert isinstance(I, CommonProp), "Not a Common property"
