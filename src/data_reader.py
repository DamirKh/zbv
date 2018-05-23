# SCADA file data reader
import csv
import datetime
import logging
import os
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import h5py  # HDF5 support

from config_case import NORMALISE_DICT

__ver__ = '1.0.1'

# StampWorld = 'Timestamp', 'DATA QUALITY'
StampWorld = ('Timestamp',)
Lang = ['ru', 'en']

mon_ru = {'янв': 1,
          'фев': 2,
          'мар': 3,
          'апр': 4,
          'май': 5,
          'июн': 6,
          'июл': 7,
          'авг': 8,
          'сен': 9,
          'окт': 10,
          'ноя': 11,
          'дек': 12
          }


def parse_date(_data_string):
    "S string"
    # data string example '02.мар.2018 23:56:44'
    _date = int(_data_string[0:2])
    _mon = mon_ru[_data_string[3:6]]
    _year = int(_data_string[7:11])
    _h, _m, _s = _data_string[12:].split(':', maxsplit=2)
    _h = int(_h)
    _m = int(_m)
    _s = int(_s)
    dt = datetime.datetime(_year, _mon, _date, _h, _m, _s)
    return dt


def parse_tag(tag_string):
    """_:type """
    # tagname found analog.P0034SB_PT0004_PV.curval
    return tag_string.split('.', maxsplit=2)[1]


def running_mean(l, N):
    """
    The running mean function
    :param l: numpy array
    :param N: window size
    :return: numpy array
    """
    # https://stackoverflow.com/a/41420229/8124158
    # Also works for the(strictly invalid) cases when N is even.
    if (N // 2) * 2 == N:
        N = N - 1
    front = np.zeros(N // 2)
    back = np.zeros(N // 2)

    for i in range(1, (N // 2) * 2, 2):
        front[i // 2] = np.convolve(l[:i], np.ones((i,)) / i, mode='valid')
    for i in range(1, (N // 2) * 2, 2):
        back[i // 2] = np.convolve(l[-i:], np.ones((i,)) / i, mode='valid')
    return np.concatenate([front, np.convolve(l, np.ones((N,)) / N, mode='valid'), back[::-1]])


class ScadaDataFile(object):
    """All methods to load data file"""

    def __init__(self):
        self.derivatives = self.ad_dydt, self.ad_shift, self.ad_normalise, self.ad_running_mean
        # self._path_to_file = path_to_file
        self.config = {'zbv version': __ver__}
        self.ss_data_present = False
        self.ss_filled = False
        self._not_saved = False

    @property
    def ss_data_saved(self):
        return not self._not_saved

    def import_data_from_csv(self, path_to_file, callback_func=None):
        """This method is for import data from SCADA OASyS"""
        if not os.path.exists(path_to_file):
            logging.error('File not exist! <<%s>>' % path_to_file)
            raise FileNotFoundError
        self.callback_func = callback_func
        f = open(path_to_file, newline='', encoding='windows-1251')
        csv_data_iterator = csv.reader(f, dialect='excel-tab')

        # First rollover. Find Tags and calculate time
        tags = set()
        time_start = datetime.datetime(2027, 9, 27)
        time_stop = datetime.datetime(1973, 10, 17)
        for row in csv_data_iterator:
            # VerboseFunc(row)
            if len(row) < 3:
                continue  # empty string
            if (row[0],) == StampWorld:
                # tagname found analog.P0034SB_PT0004_PV.curval
                tag_name = parse_tag(row[1])
                tags.add(tag_name)
            else:
                dt = parse_date(row[0])
                if dt < time_start:  # found time earlier start time
                    time_start = dt
                    # VerboseFunc("Start ", self.time_start)
                if dt > time_stop:  # found time later then stop time
                    time_stop = dt
        # End of first rollover. Find Tags and calculate time

        f.seek(0)
        current_tag = None
        timerange = pd.date_range(time_start, time_stop, freq='S')
        self.config['freq'] = 'S'
        self.config['freq in Secs'] = 1
        mesivo = pd.DataFrame(index=timerange, columns=list(tags).sort())

        for row in csv_data_iterator:
            if len(row) < 1: continue  # incomplete or empty string
            if row[0][0] == '#': continue  # comment string

            if (row[0],) == StampWorld:
                # tagname found
                current_tag = row[1]  # tag name as string
                assert isinstance(current_tag, type(''))
                current_tag = parse_tag(current_tag)
            else:
                # data found
                if current_tag is None: continue  # all data before first tag name will be passed away
                try:
                    dt = parse_date(row[0])
                    mesivo.at[dt, current_tag] = float(row[1])
                except IndexError:
                    logging.error(dt)
                    continue
        if not self.ss_data_present:
            self.data = mesivo
        else:
            print('Data merge not implemented. \n   All data replaced!')
            self.data = mesivo
        self._not_saved = True
        self.ss_data_present = True

    def fill_na_data(self):
        if not self.ss_data_present:
            return
        # filling missing data forward
        # mesivo = mesivo.ffill()
        self.data.fillna(method='ffill', inplace=True)

        # filling missing data backward
        self.data.fillna(method='bfill', inplace=True)
        self.ss_filled = True

    @property
    def tags_list(self):
        return list(self.data.columns)

    @property
    def tags(self):
        return set(self.tags_list)

    @property
    def time_start(self):
        return self.data.first_valid_index()

    @property
    def time_stop(self):
        return self.data.last_valid_index()

    @property
    def time_delta(self):
        return self.time_stop - self.time_stop

    def save_data(self, filename):
        self.data.to_hdf(filename, key='zbvdata')
        logging.info("Data file '%s' saved" % filename)
        f = h5py.File(filename, 'a')
        f.attrs['zbv_meta'] = pickle.dumps(self.config, protocol=0)
        logging.debug('Meta info saved')
        f.close()
        self._not_saved = False

    def load_data(self, filename):
        logging.info("loading data from '%s' file" % filename)
        self.data = pd.read_hdf(filename, key='zbvdata')
        logging.info("Data file '%s' loaded" % filename)
        f = h5py.File(filename, 'r')
        self.config = pickle.loads(f.attrs['zbv_meta'])
        logging.debug('Meta info loaded')
        f.close()
        self.ss_data_present = True

    def show_me_data(self, tag_names=None, reduced=False):
        # plt.figure()
        if reduced:
            reduced_sample_rate = '%iS' % self.config['freq in Secs']*60
            df = self.data.resample(reduced_sample_rate).max()
        else:
            df = self.data

        if tag_names is None:
            df.plot()
        else:
            df[tag_names].plot()
        plt.legend(loc='best')
        plt.show()

    def ad_normalise(self, tag, normalise_dict=NORMALISE_DICT, force_auto=False):
        """Normalize"""
        # pd ok
        # https://stackoverflow.com/questions/10149416/numpy-modify-array-in-place

        try:
            sensor_type = tag.split('_', maxsplit=2)[1][0:2].upper()
        except IndexError:
            sensor_type = '**'
        logging.debug("Normalize Tag %s with sensor type %s" % (tag, sensor_type))
        try:
            sensor_range = normalise_dict[sensor_type]
        except KeyError:
            # DONE: replace it wis auto range
            sensor_range = normalise_dict['other']
            sensor_range.min = self.tag_min(tag)
            sensor_range.max = self.tag_max(tag)

        if force_auto:
            sensor_range = normalise_dict['other']
            sensor_range.min = self.tag_min(tag)
            sensor_range.max = self.tag_max(tag)

        deriv_tag_name = '%s#norm' % tag  # имя добавляемого нормализованного тега

        # нормализованные данные вдоль временнОй оси
        # y = (x - min) / (max - min)
        # self.data[..., self.tags_list.index(tag)] = (self.data[
        #                                                  ..., self.tags_list.index(tag)] - sensor_range.min) / (
        #                                                         sensor_range.max - sensor_range.min)
        norm = (self.get_tag(tag) - sensor_range.min) / (sensor_range.max - sensor_range.min)
        self.data[deriv_tag_name] = norm

    def tag_min(self, tagname):
        """Returns minimum value of given tag from mesivo"""
        Min = self.data[tagname].min()
        return Min

    def tag_max(self, tagname):
        """Returns maximum value of given tag from mesivo"""
        Max = self.data[tagname].max()
        return Max

    def get_tag(self, tagname):
        """returns array slice with specified tag data"""
        return self.data[tagname]

    def delete_tag(self, tagname):
        """delete data column by tagname"""
        del (self.data[tagname])

    def ad_dydt(self, tagname):
        """Derivative (dy/dt)"""
        # pd ok
        # adding derivative of given tag to mesivo

        deriv_tag_name = '%s#dydt' % tagname
        dydt = self.data[tagname].diff()

        self.data[deriv_tag_name] = dydt

    def ad_shift(self, tagname, value):
        """Shift value *float"""
        # pd ok
        deriv_tag_name = '%s#%+.1f' % (tagname, value)
        sh = self.data[tagname] + value
        self.data[deriv_tag_name] = sh

    def ad_running_mean(self, tagname, window_size=10):
        """Running mean"""
        # pd ok
        window = '%iS' % window_size
        deriv_tag_name = '%s#RM%i' % (tagname, window_size)
        tagdata = self.data[tagname]
        rm = tagdata.rolling(window).mean()
        # rm = running_mean(tagdata, window_size)
        self.data[deriv_tag_name] = rm

    def ad_running_mean_adv(self, tagname, window_size=10):
        """Running mean centered"""
        # pd ok
        deriv_tag_name = '%s#RMC%i' % (tagname, window_size)
        tagdata = self.data[tagname]
        rm = running_mean(tagdata, window_size)
        self.data[deriv_tag_name] = rm

    def ad_running_mean_weight(self, tagname, window_size=10):
        """Exp moving averages"""
        # pd ok
        # window = '%iS' % window_size  #can't use timed window size with win_type='gaussian'
        deriv_tag_name = '%s#EMA%i' % (tagname, window_size)
        tagdata = self.data[tagname]
        rm = tagdata.rolling(window=window_size, win_type='gaussian', center=True, min_periods=1).mean(std=0.9)
        self.data[deriv_tag_name] = rm

    def export_2excel(self, filename, sheet_name='zbv_data', tags_list=None):
        if tags_list is None:
            self.data.to_excel(filename, sheet_name, na_rep='NA')
        else:
            assert isinstance(tags_list, list)
            self.data[tags_list].to_excel(filename, sheet_name, na_rep='NA')

    def import_from_excel(self, filename, sheet_name='zbv_data'):
        # Returns a DataFrame
        self.data = pd.read_excel(filename, sheet_name=sheet_name, na_rep='NA')
        self.config['freq in Secs'] = 0
        self.ss_data_present = True
        self.ss_filled = True
        self._not_saved = True

    def ad_std_deviation(self, tagname, window_size=10):
        """Standard deviation"""
        # pd ok
        deriv_tag_name = '%s#SD%i' % (tagname, window_size)
        tagdata = self.data[tagname]
        sd = tagdata.rolling(window=window_size, center=True).std()
        # rm = running_mean(tagdata, window_size)
        self.data[deriv_tag_name] = sd



if __name__ == '__main__':
    data_path = '../../data'
    if os.path.exists(os.path.join(data_path, '2Dx2.meta')):
        s = ScadaDataFile()
        s.load_data(os.path.join(data_path, '2Dx2'))
    else:
        s = ScadaDataFile()
        s.import_data_from_csv(os.path.join(data_path, '2Dx2.txt'))
        s.save_data(os.path.join(data_path, '2Dx2'))
    s.show_me_data()

    print('Ok!')
