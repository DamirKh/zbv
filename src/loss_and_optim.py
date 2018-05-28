from collections import OrderedDict
import logging

from keras import optimizers

from layers_opt import CommonLayerConfig
from layers_opt import CommonProp, BoolProp, SelectOneProp, IntRangeProp, RealRangeProp

class CommomLossConfig(CommonLayerConfig):
    pass

class CommonOptimizerConfig(CommonLayerConfig):
    def get_KERAS_optimizer(self, **overload):
        d = dict(self.get_config_as_dict())
        logging.debug("Optimizer")
        d.update(overload)
        logging.debug(d)
        Optimizer = self.create_optimizer_instance(**d)
        return Optimizer

    def create_optimizer_instance(self, **d):
        raise NotImplemented

def lr_helper(value=0.01):
    return RealRangeProp((0.,10.), description='Learning rate', value=value)

class optimizerSGD(CommonOptimizerConfig):
    """SGD https://keras.io/optimizers/#sgd"""
    def __init__(self):
        self.www = r"https://keras.io/optimizers/#sgd"
        config = OrderedDict([
            ('lr', lr_helper(0.01)),
            ('momentum', RealRangeProp((0,10),
                                       description='Parameter that accelerates SGD in the relevant direction and dampens oscillations',
                                       value=0.0)),
            ('decay', RealRangeProp((0,100),
                                    description='Learning rate decay over each update',
                                    value=0.0)),
            ('nesterov', BoolProp(description='Whether to apply Nesterov momentum',
                                  state=False)),
        ])

        super().__init__(name="SGD optimizer", config_dict=config,)

    def create_optimizer_instance(self, **d):
        return optimizers.sgd(**d)


class optimizerRMSprop(CommonOptimizerConfig):
    """RMSprop https://keras.io/optimizers/#rmsprop"""
    def __init__(self):
        self.www = r'https://keras.io/optimizers/#rmsprop'
        config = OrderedDict([
            ('lr', lr_helper(0.01)),
        ])
        super().__init__(name="RMSprop optimizer", config_dict=config)

    def create_optimizer_instance(self, **d):
        return optimizers.rmsprop(**d)



class optimizerAdagrad(CommonOptimizerConfig):
    """Adagrad https://keras.io/optimizers/#adagrad"""
    def __init__(self):
        self.www = r'https://keras.io/optimizers/#adagrad'
        super().__init__(name='Adagrad optimizer')
    def create_optimizer_instance(self, **d):
        return optimizers.adagrad(**d)


class optimizerAdadelta(CommonOptimizerConfig):
    """Adadelta https://keras.io/optimizers/#adadelta"""
    def __init__(self):
        self.www = r'https://keras.io/optimizers/#adadelta'
        super().__init__(name='Adadelta optimizer')
    def create_optimizer_instance(self, **d):
        return optimizers.adadelta(**d)


class optimizerAdam(CommonOptimizerConfig):
    """Adam https://keras.io/optimizers/#adam"""
    def __init__(self):
        self.www = r'https://keras.io/optimizers/#adam'
        super().__init__(name='Adam optimizer')
    def create_optimizer_instance(self, **d):
        return optimizers.adam(**d)


class optimizerAdamax(CommonOptimizerConfig):
    """Adamax https://keras.io/optimizers/#adamax"""
    def __init__(self):
        self.www = r'https://keras.io/optimizers/#adamax'
        super().__init__(name='Adamax optimizer')
    def create_optimizer_instance(self, **d):
        return optimizers.adamax(**d)


class optimizerNadam(CommonOptimizerConfig):
    """Nadam https://keras.io/optimizers/#nadam"""
    def __init__(self):
        self.www = r'https://keras.io/optimizers/#Nadam'
        super().__init__(name='Nadam optimizer')
    def create_optimizer_instance(self, **d):
        return optimizers.nadam(**d)


loss_functions=(
    'mean_squared_error',
    'mean_absolute_error',
    'mean_absolute_percentage_error',
    'mean_squared_logarithmic_error',
    'squared_hinge',
    'hinge',
    'categorical_hinge',
    'logcosh',
    'categorical_crossentropy',
    'sparse_categorical_crossentropy',
    'binary_crossentropy',
    'kullback_leibler_divergence',
    'poisson',
    'cosine_proximity',)

DEFINED_OPTIMIZERS = [optimizerSGD, optimizerRMSprop, optimizerAdagrad, optimizerAdadelta,
                      optimizerAdam, optimizerAdamax, optimizerNadam]
# end