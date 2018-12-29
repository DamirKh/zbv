# SCADA file data reader
import csv
import datetime
import logging
import os
import pickle

# https://pypubsub.readthedocs.io/en/v4.0.0/usage/usage_advanced_maintain.html#specify-topic-tree-def
from wx.lib.pubsub import pub
import topic_def

pub.addTopicDefnProvider(topic_def, pub.TOPIC_TREE_FROM_CLASS)
pub.setTopicUnspecifiedFatal(True)
# print(pub.exportTopicTreeSpec()) unusable while message really go via te pubsub

import matplotlib

matplotlib.use('WXAgg')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import h5py  # HDF5 support

from config_case import NORMALISE_DICT
from constants import HIDDEN_DATA
from MyExceptions import BadUserError

# from scipy import interpolate

__ver__ = 1.1
# ScadaDataFile.config добавлено хранение списка скрытых наборов fake данных.

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

norma = '=NORMA='
alarm = '=ALARM='


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
    """ returns center part of tag name. i.e. if tag_string analog.P0034SB_PT0004_PV.curval
     function returns P0034SB_PT0004_PV"""
    # tagname found analog.P0034SB_PT0004_PV.curval
    try:
        center_name = tag_string.split('.', maxsplit=2)[1]
    except IndexError:
        center_name = tag_string
    return center_name


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
        self.fit_data = {}
        self.derivatives = self.ad_dydt, self.ad_shift, self.ad_normalise, self.ad_running_mean
        # self._path_to_file = path_to_file
        self.config = {'zbv version': __ver__}
        self.config = {HIDDEN_DATA: []}
        self.ss_data_present = False
        self.ss_filled = False
        self._not_saved = False
        pub.sendMessage(topic_def._zbv_data, msg="SCADA data fileobject inited")

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
        # End of first rollover. Tags found and time calculated.

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

    def import_data_from_real_csv(self, path_to_file, callback_func=None):
        """This method is for import data from csv file, like from Siemens turbine"""
        if not os.path.exists(path_to_file):
            logging.error('File not exist! <<%s>>' % path_to_file)
            raise FileNotFoundError
        self.callback_func = callback_func

        self.config['freq'] = ''
        self.config['freq in Secs'] = 0

        mesivo = pd.read_csv(path_to_file, skiprows=1, index_col=0, parse_dates=True)

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

    def interpolate(self, tag, method):
        if tag[-1] == '=':  # последний символ "=" означает не генерировть деривативы от этого тега
            raise BadUserError("Use real tag!", tag)
        deriv_tag_name = '%s#INTER' % tag
        inter = self.data[tag].interpolate(method)
        self.data[deriv_tag_name] = inter

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
        store = pd.HDFStore(filename, mode='w')
        store['zbvdata'] = self.data
        logging.info("Data file '%s' saved" % filename)

        for name_of_hidden_data in self.config[HIDDEN_DATA]:
            hidden_frame = self.fit_data[name_of_hidden_data]
            assert isinstance(hidden_frame, pd.DataFrame)
            store[name_of_hidden_data] = hidden_frame
            logging.info("Hidden frame '%s' saved" % name_of_hidden_data)
        store.close()

        f = h5py.File(filename, 'a')
        f.attrs['zbv_meta'] = pickle.dumps(self.config, protocol=0)
        logging.debug('Meta info saved')
        f.close()

        self._not_saved = False

    def load_data(self, filename):
        logging.info("loading data from '%s' file" % filename)

        f = h5py.File(filename, 'r')
        self.config = pickle.loads(f.attrs['zbv_meta'])
        f.close()
        logging.debug('Meta info loaded from file <%s>' % filename)

        store = pd.HDFStore(filename, mode='r')
        self.data = store['zbvdata']
        logging.info("Data loaded from file '%s'" % filename)

        print("Config say file contain next hidden data")
        print(self.config[HIDDEN_DATA])
        for name_of_hidden_data in self.config[HIDDEN_DATA]:
            hidden_frame = store[name_of_hidden_data]
            assert isinstance(hidden_frame, pd.DataFrame)
            self.fit_data[name_of_hidden_data] = hidden_frame
            logging.info("Hiden frame '%s' loaded" % name_of_hidden_data)
        store.close()
        self.ss_data_present = True

    def show_me_data(self, tag_names=None, reduced=False):
        # simple and dirty
        # plt.figure()
        if reduced:
            reduced_sample_rate = '%iS' % self.config['freq in Secs'] * 60
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
        self.update_hidden_data()
        self.check_hidden_frames()

    def tag_min(self, tagname):
        """Returns minimum value of given tag from mesivo"""
        try:
            Min = self.data[tagname].min()
        except ValueError:
            Min = 0.
        return Min

    def tag_max(self, tagname):
        """Returns maximum value of given tag from mesivo"""
        try:
            Max = self.data[tagname].max()
        except ValueError:
            Max = 0.
        return Max

    def get_tag(self, tagname):
        """returns array slice with specified tag data"""
        return self.data[tagname]

    def delete_tag(self, tagname):
        """delete data column by tagname"""
        # todo добавить удаление скрытых тренировочных данных при удалении tagname
        assert isinstance(tagname, str)

        try:

            if tagname == norma:  # удаляем все тренировочные данные
                for flag in self.fit_data.keys():  # все флаги
                    del (self.data[flag])

                self.fit_data = {}  # сбрасываем тренировочные наборы
                self.config[HIDDEN_DATA] = []  #
                self.config['CROSS'] = False  # признак наличия данных кросс-тренировки
                del (self.data[tagname])
                return

            alarm_tag = tagname + alarm  # нужно проверить и этот тег

            if tagname.endswith(alarm):  # если пользователь удаляет флаг
                del self.fit_data[tagname]  # удалить тренировочные данные тоже

            if alarm_tag in self.tags_list:  # если пользователь удаляет тег, у которого есть флаг
                del self.fit_data[alarm_tag]  # удалить этого тега флаг и тренировочные данные
                del self.data[alarm_tag]

            del (self.data[tagname])  # здесь удаляем тег, который просили удалить
        except KeyError:
            print("Error while deleting!")
            pass
        self.config[HIDDEN_DATA] = list(self.fit_data.keys())
        self.update_hidden_data()
        self.check_hidden_frames()

    def ad_dydt(self, tagname):
        """Derivative (dy/dt)"""
        # pd ok
        # adding derivative of given tag to mesivo
        if tagname[-1] == '=':  # последний символ "=" означает не генерировть деривативы от этого тега
            raise BadUserError("Use real tag!", tagname)
        deriv_tag_name = '%s#dydt' % tagname
        dydt = self.data[tagname].diff()

        self.data[deriv_tag_name] = dydt
        self.update_hidden_data()
        self.check_hidden_frames()

    def ad_abs(self, tagname):
        """Absolute"""
        if tagname[-1] == '=':  # последний символ "=" означает не генерировть деривативы от этого тега
            raise BadUserError("Use real tag!", tagname)
        deriv_tag_name = '%s#ABS' % tagname
        abst = self.data[tagname].abs()

        self.data[deriv_tag_name] = abst
        self.update_hidden_data()
        self.check_hidden_frames()

    def ad_shift(self, tagname, value):
        """Shift value *float"""
        # pd ok
        if tagname[-1] == '=':  # последний символ "=" означает не генерировть деривативы от этого тега
            raise BadUserError("Use real tag!", tagname)

        deriv_tag_name = '%s#%+.1f' % (tagname, value)
        sh = self.data[tagname] + value
        self.data[deriv_tag_name] = sh
        self.update_hidden_data()
        self.check_hidden_frames()

    def ad_running_mean(self, tagname, window_size=10):
        """Running mean"""
        # pd ok
        if tagname[-1] == '=':  # последний символ "=" означает не генерировть деривативы от этого тега
            raise BadUserError("Use real tag!", tagname)

        window = '%iS' % window_size
        deriv_tag_name = '%s#RM%i' % (tagname, window_size)
        tagdata = self.data[tagname]
        rm = tagdata.rolling(window).mean()
        # rm = running_mean(tagdata, window_size)
        self.data[deriv_tag_name] = rm
        self.update_hidden_data()
        self.check_hidden_frames()

    def ad_running_mean_adv(self, tagname, window_size, in_sec):
        """Running mean centered"""
        # pd ok
        if tagname[-1] == '=':  # последний символ "=" означает не генерировть деривативы от этого тега
            raise BadUserError("Use real tag!", tagname)

        deriv_tag_name = '%s#RMC%i' % (tagname, in_sec)
        tagdata = self.data[tagname]
        rm = running_mean(tagdata, window_size)
        self.data[deriv_tag_name] = rm
        self.update_hidden_data()
        self.check_hidden_frames()

    def ad_running_mean_weight(self, tagname, window_size=10):
        """Exp moving averages"""
        # pd ok
        # window = '%iS' % window_size  #can't use timed window size with win_type='gaussian'
        if tagname[-1] == '=':  # последний символ "=" означает не генерировть деривативы от этого тега
            raise BadUserError("Use real tag!", tagname)
        deriv_tag_name = '%s#EMA%i' % (tagname, window_size)
        tagdata = self.data[tagname]
        rm = tagdata.rolling(window=window_size, win_type='gaussian', center=True, min_periods=1).mean(std=0.9)
        self.data[deriv_tag_name] = rm
        self.update_hidden_data()
        self.check_hidden_frames()

    def export_2excel(self, filename, sheet_name='zbv_data', tags_list=None, debug=True):
        if tags_list is None:
            self.data.to_excel(filename, sheet_name, na_rep='NA')
        else:
            assert isinstance(tags_list, list)
            self.data[tags_list].to_excel(filename, sheet_name, na_rep='NA')
        if debug:
            splited_name = os.path.splitext(filename)
            for N, hidden_df in enumerate(self.fit_data.items(), start=1):
                assert isinstance(hidden_df[1], pd.DataFrame)
                print('Export %s into:' % hidden_df[0])
                print('      %s_%i%s' % (splited_name[0], N, splited_name[1]))
                hidden_df[1].to_excel('%s_%i%s' % (splited_name[0], N, splited_name[1]),
                                      sheet_name=hidden_df[0],
                                      na_rep='NA')

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
        if tagname[-1] == '=':  # последний символ "=" означает не генерировть деривативы от этого тега
            raise BadUserError("Use real tag!", tagname)
        deriv_tag_name = '%s#SD%i' % (tagname, window_size)
        tagdata = self.data[tagname]
        sd = tagdata.rolling(window=window_size, center=True).std()
        # rm = running_mean(tagdata, window_size)
        self.data[deriv_tag_name] = sd
        self.update_hidden_data()
        self.check_hidden_frames()

    def update_hidden_data(self):
        # update all hidden dataframes
        for tag, prev_df in self.fit_data.items():  # prev_df  - ранее сгенерированный <тренировочный набор>
            print("update fitting data for <%s>" % tag)
            for missing_tag in self.tags - set(
                    list(prev_df.columns)):  # добавление недостающих тегов в <тренировочный набор>
                prev_df.loc[:, missing_tag] = self.data.loc[:, missing_tag]
                print("Add missing tag <%s>" % missing_tag)
            for waste_tag in set(list(prev_df.columns)) - self.tags:  # удаление тегов из <тренировочного набора>,
                # если эти теги отсутствуют в <ориганальной таблице>
                del prev_df[waste_tag]
                print("Delete waste tag <%s>" % waste_tag)

    def check_hidden_frames(self):
        # проверка правильности генерации <тренировочных наборов>
        # список тегов всех dataframe должен совпадать
        for df in self.fit_data.values():
            if self.tags == set(list(df.columns)):
                continue
            else:
                raise ValueError("Different fit set!", self.tags, set(list(df.columns)))

    def generate_fitting_data(self, tagname, debug=True):
        assert isinstance(tagname, str)
        print("Generate fitting data")

        alarm_tag = tagname + alarm  # alarm_tag - также нужно использовать в качестве выходного тега

        if tagname[-1] == '=':  # последний символ "=" означает НЕ генерировть <тренировочный набор> на этом теге
            raise BadUserError("Use real tag!", alarm_tag)

        df = self.data  # для краткости
        # first, create NORMA for origin table if still missing
        if norma not in self.tags_list:
            df.loc[:, norma] = np.array([1] * len(df))
        # create TAGNAME=ALARM= for origin table if missing
        if alarm_tag not in self.tags_list:  # проверяем по наличию уже сгенерированного тега TAGNAME=ALARM=
            df.loc[:, alarm_tag] = np.array([0] * len(df))
        else:
            raise BadUserError("This tag has got fit data already!", alarm_tag)

        mesivo = self.data.copy()
        mesivo.loc[:, norma] = np.array([0] * len(mesivo))
        mesivo.loc[:, alarm_tag] = np.array([1] * len(mesivo))
        mesivo.loc[:, tagname] = -mesivo.loc[:, tagname]  # конкретно эта формула задает тип тренировочных данных
        # в данном случае это простая инверсия. Ее можно использовать на тегах-производных (производная
        # в математическом смысле, а не просто унаследованная от реального тега) от реальных тегов (dy/dt)
        # и тут возникает проблема: если производная оригинала = 0, то инвертированная производная тоже =0
        #  считать нулевое значение подделкой или достоверными данными?
        # попробуем для подделки - инверсии считать, что  0 - достоверные данные.
        # https://stackoverflow.com/a/38467449/8124158
        # df.loc[df[ < some_column_name >] == < condition >, < another_column_name >] = < value_to_add >
        # df.loc[df['B'] ==0, 'D'] = 666.
        mesivo.loc[mesivo[tagname] == 0, alarm_tag] = 0.
        mesivo.loc[mesivo[alarm_tag] == 0, norma] = 1.

        # на тегах других типов тоже можно, но смысла нет. TODO в гуе спросить у пользователя подтверждение если
        # имя тега не содержит #dydt
        # проблема может возникнуть если удалить из <оригинальной таблицы> tagname
        # done: добавить удаление скрытых тренировочных данных при удалении tagname

        if debug:
            df['%s!FIT' % tagname] = mesivo.loc[:, tagname]

        self.fit_data[alarm_tag] = mesivo  # Как это сохранить? Сделано уже. См метод save_data
        self.config[HIDDEN_DATA] = list(self.fit_data.keys())

        self.update_hidden_data()
        self.check_hidden_frames()
        self.config['CROSS'] = True
