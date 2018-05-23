from keras.preprocessing.sequence import TimeseriesGenerator
from constants import *
from data_reader import ScadaDataFile
# https://stackoverflow.com/questions/50322660/custom-data-generator-for-keras-lstm-with-timeseriesgenerator

class MyTimeseriesGenerator(TimeseriesGenerator):
    # https://keras.io/preprocessing/sequence/#timeseriesgenerator
    def __init__(self, zbv_model_config, zbv_data):
        assert isinstance(zbv_data, ScadaDataFile)
        self.zbv_model_config = zbv_model_config
        self.zbv_data = zbv_data
        input_tags = list(zbv_model_config[INPUT_TAGS_NAMES])
        output_tags = list(zbv_model_config[OUTPUT_TAGS_NAMES])

        print(zbv_data.data[input_tags])
        data = zbv_data.data[input_tags].values
        print(zbv_data.data[output_tags])
        targets = zbv_data.data[output_tags].values

        # TimeseriesGenerator(data, targets, length, sampling_rate=1, stride=1, start_index=0, end_index=None, shuffle=False, reverse=False, batch_size=128)
        super().__init__(data, targets, length= zbv_model_config[WINDOW_SIZE], shuffle=True)
        pass

    def __getitem__(self, index):
        samples, targets = super().__getitem__(index)
        # print(samples)
        # print(targets)
        return samples, targets

    def on_epoch_end(self):
        """Method called at the end of every epoch"""
        pass