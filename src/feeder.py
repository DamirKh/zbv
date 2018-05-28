import random
from keras.preprocessing.sequence import TimeseriesGenerator
from constants import *
from data_reader import ScadaDataFile
import pandas as pd

random.seed()

# https://stackoverflow.com/questions/50322660/custom-data-generator-for-keras-lstm-with-timeseriesgenerator

class MyTimeseriesGenerator(TimeseriesGenerator):
    # https://keras.io/preprocessing/sequence/#timeseriesgenerator
    def __init__(self, zbv_model_config, zbv_data, batch_size=128, no_targets=False, cross=False):
        assert isinstance(zbv_data, ScadaDataFile)
        self.cross = cross
        self.zbv_model_config = zbv_model_config
        self.zbv_data = zbv_data
        input_tags = list(zbv_model_config[INPUT_TAGS_NAMES])
        output_tags = list(zbv_model_config[OUTPUT_TAGS_NAMES])

        # Main generator
        # print(zbv_data.data[input_tags])
        data = zbv_data.data[input_tags].values
        # print(zbv_data.data[output_tags])
        if no_targets:  # will be used while prediction. No targets available
            targets = zbv_data.data[input_tags].values
        else:
            targets = zbv_data.data[output_tags].values
        # TimeseriesGenerator(data, targets, length, sampling_rate=1, stride=1, start_index=0, end_index=None, shuffle=False, reverse=False, batch_size=128)
        super().__init__(data, targets, length=zbv_model_config[WINDOW_SIZE], batch_size=batch_size)  # shuffle=True

        # auxiliary generators
        if self.cross:
            self._aux_gens = {}
            # включаем в список дополнительных генераторов только те, что есть в <тренировочных наборах>
            # и в списке выходных тегов
            trainable_tags = set(output_tags).intersection(set(zbv_data.fit_data.keys()))
            for trainable_tag in trainable_tags:
                df = zbv_data.fit_data[trainable_tag]
                assert isinstance(df, pd.DataFrame)
                data = df[input_tags].values
                targets = df[output_tags].values
                self._aux_gens[trainable_tag] = TimeseriesGenerator(data, targets, length=zbv_model_config[WINDOW_SIZE], batch_size=batch_size)
            print("CROSS Fit generators datasets:\n", self._aux_gens.keys())
            self._allgens = []
            self._allgens.append(None)
            # разбавим плотность <тренировочных наборов> <оригинальной таблицей>
            for gen in self._aux_gens.values():
                self._allgens.append(gen)
                self._allgens.append(None)

    def __getitem__(self, index):
        if self.cross:
            random_gen = random.choice(self._allgens)
            if random_gen is not None:
                #print("Fake data feeded...")
                samples, targets = random_gen[index]
            else:
                #print("Real data feeded...")
                samples, targets = super().__getitem__(index)
        else:
            samples, targets = super().__getitem__(index)
        self.after_get_item_call(index)
        return samples, targets

    def after_get_item_call(self, index):
        pass

    def on_epoch_end(self):
        """Method called at the end of every epoch"""
        pass
