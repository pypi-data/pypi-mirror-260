import datetime
import logging
import os
import sys
import lightgbm as lgb
import numpy as np
import pandas as pd
from matplotlib import gridspec
from scipy.io import savemat, loadmat

from lmsleepdata.data_load import data_loader
from lmsleepdata.functions.biomarker import sw_detect, spindles_detect
from lmsleepdata.functions.feature_extract import RSCFeature, WearDectectFeature
from lmsleepdata.functions.sleep_staging import sleep_staging_with_features, load_model
from lmsleepdata.functions.wear_detect import wear_detect_with_features
import matplotlib.pyplot as plt
import seaborn as sns
from lmsleepdata.pdf.pdf_generator import report_pdf_generator, gen_pdf_ar4
from lmsleepdata.plots.sleep_staging_plot import plot_spectrogram, plot_avg_diff_acc, plot_sleep_staging_result_5c, \
    plot_sleep_posture, plot_sleep_staging_result_4c
from lmsleepdata.plots.stim_plot import plot_stim_sham_sw
from lmsleepdata.functions.sleep_variable_compute import *
from lmsleepdata.preprocess.filter import eeg_filter
from lmsleepdata.functions.posture_analyse import sleep_posture_analyse
from lmsleepdata.predict_with_sleepyco_net import predict_with_raw_eeg


class DataHandler(object):
    def __init__(self):

        self.raw_eeg = None
        self.raw_eeg_another = None
        self.staging_mode = None
        self.class_count = None
        self.disconnections = None
        self.end_time = None
        self.start_time = None
        self.package_loss_rate = None
        self.disconnect_rate = None
        self.data_path = None
        self.record_info = {}
        self.patient_info = {}
        self.analysis_fig_path = None
        self.data_preview_fig_path = None
        self.sleep_postures = None
        self.raw_sti = None
        self.data_name = None
        self.logger = None
        self.sleep_variables = None
        self.seconds = None
        self.sp_df = None
        self.sleep_staging_result = None
        self.acc = None
        self.eeg = None
        self.eeg_another = None
        self.biomarker = None
        self.features = pd.DataFrame({})
        self.supported_features = {}
        self.sf_eeg = 500
        self.sf_acc = 50
        self.epoch_len = 15
        self.sw_df = None
        self.data_type = 'X7'
        self.set_logger()

    def set_logger(self):
        """
        设置日志输出格式，一般不用设置
        存在问题，和依赖的框架（如LightGBM）的日志似乎有冲突，字体颜色等不能设置成想要的格式
        :return:
        """
        self.logger = logging.getLogger("LM Data Handler")
        self.logger.setLevel("INFO")
        # 创建一个handler，用于输出日志到控制台
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s: %(message)s'
        )
        # 将formatter添加到handler
        console_handler.setFormatter(formatter)
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)
        # 将handler添加到logger
        self.logger.addHandler(console_handler)

    def set_data_type(self, data_type):
        """
        设置数据格式：X7/X8，两种数据的解析和处理流程存在差异
        :param data_type:
        :return:
        """
        assert data_type in {"X7", "X8"}, "Unsupported data type, only X7/X8 is allowed."
        self.data_type = data_type

    def predict_with_single_epoch(self, eeg, acc, clf, cached_feature_arr):
        """
        专用于X8实时后台分期，算法flask服务接受终端单个epoch数据，经过解析、预处理后，调用该方法获取单个epoch的睡眠分期结果
        20240103：
            4分类，无异常状态分类（佩戴检测待做）；
            仅使用eeg特征，无acc特征；
        :param eeg: 脑电数据
        :param acc: 体动数据（未使用）
        :param clf: LightGBM模型
        :param cached_feature_arr: 已缓存的特征
        :return: 分期结果
        """
        eeg = eeg.reshape(1, 7500)
        acc = acc.reshape(1, 3, 750)

        meta_feature = {'male': 1, 'age': 30, 'data_type': 0, 'h/w': 0}
        features = RSCFeature(meta_feature, raw_eeg=eeg, raw_acc=None,
                              sf_eeg=500, sf_acc=50, context_mode=1).get_features()
        cols_all = features.columns
        cols_simple = cols_all[
            (~cols_all.str.endswith('_norm')) &
            (~cols_all.str.startswith('male')) &
            (~cols_all.str.startswith('age')) &
            (~cols_all.str.startswith('data_type'))
            ].tolist()
        features = features[cols_simple]

        raw_feature_count = features.shape[1]
        # 排除 meta feature/p2_norm feature之后的特征
        simple_feature_count = raw_feature_count
        cached_feature = None
        if cached_feature_arr is None or len(cached_feature_arr) % simple_feature_count != 0:
            cached_feature = features
        else:
            cached_feature = pd.DataFrame(columns=features.columns)
            cached_feature_count = (len(cached_feature_arr) // simple_feature_count)

            for i in range(cached_feature_count):
                new_df = pd.DataFrame([cached_feature_arr[i * raw_feature_count:(i + 1) * raw_feature_count]],
                                      columns=features.columns)
                cached_feature = cached_feature._append(new_df, ignore_index=True)

            cached_feature = cached_feature._append(features, ignore_index=True)

        if len(cached_feature) > 9:
            cached_feature = cached_feature.iloc[1:]

        rollp = cached_feature.rolling(window=9, min_periods=1).mean()
        rollp = rollp.add_suffix("_p2min_norm")
        rollp = rollp.loc[rollp.index.max():rollp.index.max()]
        rollp = rollp.reset_index(drop=True)
        feature_for_predict = features.join(rollp)
        feature_for_predict['male'] = 1
        feature_for_predict['age'] = 30
        feature_for_predict['data_type'] = 0
        feature_for_predict = feature_for_predict[clf.feature_name()]
        raw_score = clf.predict(feature_for_predict)
        # for i in clf.feature_name():
        #     print("{}: {}".format(i, feature_for_predict[i].values[0]))
        # print("epoch: {}, raw score: {:.5f}".format(cached_feature.index.max(), max(raw_score[0])))

        if raw_score[0, 1] > 0.5:  # 如果N3的概率大于0.5
            predictions = 1
        else:
            raw_score[0, 1] = 0  # 如果N3的概率小于0.5
            predictions = np.argmax(raw_score, axis=1)

        classes_with_alphabet_order = np.array(['N1/N2', 'N3', 'REM', 'Wake'])
        predictions = classes_with_alphabet_order[predictions]
        df_hypno = pd.Series(predictions)
        df_hypno.replace({'N3': 0, 'N1/N2': 1, 'REM': 2, 'Wake': 3}, inplace=True)

        predictions = df_hypno.to_numpy()

        # todo: add wear detect res
        # wear_detect_res = self.wear_detect()
        # predictions[wear_detect_res == 0] = 5
        #
        # pp_predictions = pp_label_smooth(np.copy(predictions), window=2)
        # sleep_staging_result = pp_predictions
        # raw_feature_name =
        return int(predictions[0]), 0, cached_feature

    def load_data_file(self, data_name, eeg_path, acc_path, ble_path, sti_path, person_info=None):
        """
        加载数据文件，eeg/acc数据都会保存一份原始数据（不经过滤波和裁剪），记作raw_egg/raw_acc
        :param data_name: 数据名，一般内容包括 "phone_date_time"
        :param eeg_path: eeg文件路径
        :param acc_path: acc文件路径
        :param ble_path: ble文件路径（X8没有）
        :param sti_path: sti文件路径（X8为sti.log，X7为sti.sti）
        :param person_info: 用户基本信息（年龄、性别、身高/体重等），目前没有用，都是设置为默认值
        :return:
        """
        assert data_name is not None, "Please check the data name and retry."

        self.data_name = data_name
        raw_eeg_2_channel, eeg_2_channel, self.raw_acc, self.acc, self.raw_sti, self.disconnections, self.total_time, self.start_time, self.end_time, self.package_loss_rate, self.disconnect_rate = data_loader.load_data(
            eeg_path, acc_path, sti_path, ble_path, data_type=self.device_type, logger=self.logger)

        if self.start_time is not None:
            start_datetime_str = str(self.start_time)
            date_str = str(self.start_time)[0:10]
            self.record_info["record_start_time"] = start_datetime_str
            self.record_info["record_date"] = date_str
        if self.end_time is not None:
            end_datetime_str = str(self.end_time)
            date_str = str(self.end_time)[0:10]
            self.record_info["record_end_time"] = end_datetime_str
            self.record_info["record_date"] = date_str

        eeg_sec = -1
        acc_sec = -1
        if eeg_2_channel is not None and raw_eeg_2_channel is not None:
            self.eeg = (eeg_2_channel[0] - 32767) / 65536 * 2.5 * 1000 * 1000 / 100  #  eeg单位转换-μV
            self.raw_eeg = raw_eeg_2_channel[0]
            self.eeg = np.squeeze(self.eeg)
            eeg_sec = self.eeg.shape[0] // self.sf_eeg
            self.seconds = eeg_sec
            self.eeg_another = (eeg_2_channel[1] - 32767) / 65536 * 2.5 * 1000 * 1000 / 100  # 另一个channel的data
            self.raw_eeg_another = raw_eeg_2_channel[1]
            self.eeg_another = np.squeeze(self.eeg_another)

        if self.acc is not None and self.raw_acc is not None:
            self.acc = self.acc - 32767
            self.acc = np.squeeze(self.acc)
            acc_sec = self.acc.shape[1] // self.sf_acc

        if eeg_sec != -1 and acc_sec != -1:
            assert eeg_sec == acc_sec, "EEG length have to be consistent with ACC."

        if self.eeg is not None:
            self.eeg = self.eeg[:self.seconds * self.sf_eeg]
            self.eeg_another = self.eeg_another[:self.seconds * self.sf_eeg]
        if self.acc is not None:
            self.acc = self.acc[:self.seconds * self.sf_acc]
        self.logger.info("Data loaded, {} total seconds".format(self.seconds))

        self.features['meta'] = {'male': 1, 'age': 30, 'data_type': 0, 'h/w': 0}
        if person_info is not None:
            if person_info['male'] is not None:
                self.features['meta']['male'] = person_info['male']
            if person_info['age'] is not None:
                self.features['meta']['age'] = person_info['age']
            if person_info['data_type'] is not None:
                self.features['meta']['data_type'] = person_info['data_type']
            if person_info['height'] is not None and person_info['weight'] is not None:
                self.features['meta']['h/w'] = person_info['height'] / person_info['weight']
        return self

    def concat_data_file(self, eeg_path, acc_path, ble_path, sti_path):
        """
        拼接数据文件：
        中间的时间间隔会进行数据补0
        拼接后的数据会使用第一套数据的开始时间作为开始时间，第二套数据的结束时间作为结束时间
        拼接后的丢包率、断连率等会根据两套数据的结果进行重新计算
        :param eeg_path: 第二套数据的eeg路径
        :param acc_path: 第二套数据的acc路径
        :param ble_path: 第二套数据的ble路径
        :param sti_path: 第二套数据的sti路径
        :return:
        """
        assert self.start_time is not None and self.end_time is not None and self.raw_acc is not None and self.raw_eeg is not None, "Please load data first before concat data"
        raw_eeg, eeg, raw_acc, acc, raw_sti, disconnections, total_time, start_time, end_time, package_loss_rate, disconnect_rate = data_loader.load_data(
            eeg_path, acc_path, sti_path, ble_path, data_type=self.data_type, logger=self.logger)

        new_end_time = str(end_time)[5:7] + str(end_time)[8:10] + "-" + str(end_time)[11:13] + "_" + str(end_time)[
                                                                                                     14:16] + "_" + str(
            end_time)[17:19]
        self.data_name = self.data_name[:26] + new_end_time + self.data_name[39:]

        # self.data_name = self.data_name.replace(self.end_time, end_time)
        self.package_loss_rate = (self.package_loss_rate * self.total_time + package_loss_rate * total_time) / (
                self.total_time + total_time)

        self.disconnect_rate = (
                                       self.disconnect_rate * self.total_time + disconnect_rate * total_time + start_time.timestamp() - self.end_time.timestamp()) / (
                                       end_time.timestamp() - self.start_time.timestamp())
        if self.disconnections is not None:
            self.disconnections = np.vstack(
                [self.disconnections, np.array([[self.end_time.timestamp(), start_time.timestamp()]])])
        else:
            self.disconnections = np.array([[self.end_time.timestamp(), start_time.timestamp()]])
        if disconnections is not None:
            self.disconnections = np.vstack([self.disconnections, disconnections])

        if eeg is not None and raw_eeg is not None:
            eeg = (eeg[0] - 32767) / 65536 * 2.5 * 1000 * 1000 / 100
            raw_eeg = raw_eeg[0]
            eeg = np.squeeze(eeg)
            eeg_sec = eeg.shape[0] // self.sf_eeg
            self.seconds = self.seconds + eeg_sec

        if acc is not None and raw_acc is not None:
            acc = acc - 32767
            acc = np.squeeze(acc)
            acc_sec = acc.shape[1] // self.sf_acc

        time_gap = start_time.timestamp() - self.end_time.timestamp()
        self.raw_eeg = np.concatenate(
            (self.raw_eeg, np.zeros(round(time_gap * self.sf_eeg)).astype(self.raw_eeg.dtype), raw_eeg))
        self.raw_acc = np.concatenate(
            (self.raw_acc, np.zeros([3, round(time_gap * self.sf_acc)]).astype(self.raw_acc.dtype), raw_acc), axis=1)
        self.raw_sti = np.concatenate((self.raw_sti, raw_sti))
        self.eeg = np.concatenate((self.eeg, np.zeros(round(time_gap * self.sf_eeg)).astype(self.eeg.dtype), eeg))
        self.acc = np.concatenate((self.acc, np.zeros([3, round(time_gap * self.sf_acc)]).astype(self.acc.dtype), acc),
                                  axis=1)
        self.end_time = end_time
        end_datetime_str = str(self.end_time)
        date_str = str(self.end_time)[0:10]
        self.record_info["record_end_time"] = end_datetime_str
        self.record_info["record_date"] = date_str

    def concat_data(self, data_path):
        """
        拼接数据文件：主要针对澜猫数据可能出现的中断（区别于丢包、断连，中断前后的数据会被记录成2个独立的数据，保存并上传）
        需要用DataHandler先加载第一套数据，再调用该方法，将第二套数据拼接上来
        理论上可以拼接多套数据
        :param data_path: 第二套数据的路径
        :return:
        """
        assert os.path.exists(data_path), "The data path not exist, please check!"
        eeg_path = None
        acc_path = None
        sti_path = None
        ble_path = None
        for file in os.listdir(data_path):
            if file.endswith(".eeg"):
                eeg_path = os.path.join(data_path, file)
            if file.endswith(".acc"):
                acc_path = os.path.join(data_path, file)
            if file.endswith(".sti"):
                sti_path = os.path.join(data_path, file)
            if file.endswith(".ble"):
                ble_path = os.path.join(data_path, file)
        self.concat_data_file(eeg_path, acc_path, ble_path, sti_path)

    def load_data(self, device_type, data_name, data_path, patient_info=None):
        """
        加载数据，根据路径和数据名，找到里面每种数据的具体路径，然后调用load_data_file
        :param device_type: 数据格式（X8/X7）
        :param data_name: 数据名
        :param data_path: 数据路径
        :param patient_info: 用户信息（年龄，身高，性别），目前没有用，都是默认值
        :return:
        """
        assert data_name is not None, "Please check the data name and retry!"
        self.patient_info = patient_info
        self.data_name = data_name
        self.data_path = data_path
        self.device_type = device_type
        eeg_path = None
        acc_path = None
        sti_path = None
        ble_path = None
        if self.device_type == 'X7':
            for file in os.listdir(data_path):
                if file.endswith(".eeg"):
                    eeg_path = os.path.join(data_path, file)
                if file.endswith(".acc"):
                    acc_path = os.path.join(data_path, file)
                if file.endswith(".sti"):
                    sti_path = os.path.join(data_path, file)
                if file.endswith(".ble"):
                    ble_path = os.path.join(data_path, file)
        elif self.device_type == 'X8':
            for file in os.listdir(data_path):
                if file.endswith(".eeg"):
                    eeg_path = os.path.join(data_path, file)
                if file.endswith(".acc"):
                    acc_path = os.path.join(data_path, file)
                if file.endswith("sti.log"):
                    sti_path = os.path.join(data_path, file)
        # if os.listdir().__contains__("sti.sti"):
        #     sti_path = os.path.join(data_path, "sti.sti")
        # elif os.listdir().__contains__("sti.log"):
        #     sti_path = os.path.join(data_path, "sti.log")
        self.load_data_file(data_name, eeg_path, acc_path, ble_path, sti_path, None)
        return self

    def load_eeg_and_acc_mat(self, data_name, data_path, patient_info):
        """
        加载转换过后的mat数据（通过save_data_to_mat方法保存，一般命名为eeg_and_acc.mat）
        :param data_name: 数据名
        :param data_path: 数据路径
        :param patient_info: 用户信息（年龄，性别，身高/体重）
        :return:
        """
        assert data_name is not None, "Please check the data name and retry!"
        self.patient_info = patient_info
        self.data_name = data_name
        self.data_path = data_path
        assert os.path.exists(os.path.join(data_path, "eeg_and_acc.mat")), "eeg_and_acc.mat don't exist."
        eeg_and_acc = loadmat(os.path.join(data_path, "eeg_and_acc.mat"))
        epoch = eeg_and_acc["eeg"].squeeze().shape[0] // 7500
        self.seconds = epoch * 15
        self.raw_eeg = eeg_and_acc["eeg"].squeeze()[0:epoch * 7500]
        self.eeg = eeg_and_acc["eeg"].squeeze()[0:epoch * 7500]
        self.raw_acc = eeg_and_acc["acc"][0:epoch * 750]
        self.acc = eeg_and_acc["acc"][0:epoch * 750]
        self.epoch_len = 15
        self.features['meta'] = {'male': 1, 'age': 30, 'data_type': 0, 'h/w': 0}

    def save_data_to_mat(self, mat_path):
        """
        保存已经加载的eeg和acc到mat文件中，使用原始数据，仅进行基础的eeg单位换算。
        一般可用于在matlab、python中进行自定义的数据分析。
        :param mat_path: 待保存的路径
        :return:
        """
        if self.eeg is None:
            self.logger.info("Please load EEG data first.")
        if self.acc is None:
            self.logger.info("Please load ACC data first.")
        savemat(mat_path, {'eeg': (self.raw_eeg - 32767) / 65536 * 2.5 * 1000 * 1000 / 100, 'acc': self.raw_acc,
                           'package_loss_rate': self.package_loss_rate,
                           'disconnect_rate': -1 if self.disconnect_rate is None else self.disconnect_rate})

    def save_features_to_parquet(self, feature_path):
        """
        保存提取的特征数据。
        一般可以用于聚类或其他分析。
        :param feature_path: 待保存的路径
        :return:
        """
        if self.features is None:
            self.logger.info("Please do feature extraction first.")
        self.features.to_parquet(path=feature_path)

    def load_hypno(self, hypno):
        """
        加载分期数据，可以用于计算睡眠指标。
        不要在已经加载数据文件并进行自动分期后，再加载其他分期数据，会引起数据不一致问题。
        :param hypno: 睡眠分期数据，一维ndarray或者一维list
        :return:
        """
        hypno = np.asarray(hypno)
        if np.shape(hypno.shape) != 1 or hypno.shape[0] <= 0:
            self.logger.error("Format of hypno is incorrect, please check hypno is one-dimension array!")
            return
        if self.sleep_staging_result is not None and hypno.shape[0] != self.sleep_staging_result.shape[0]:
            self.logger.error("The length of hypno is not consistent with loaded EEG, please check!")
            return
        self.hypno = hypno
        return self

    def tailor_operation(self, tailor_type="drop_tail", tailor_param=None):
        """
        进行数据裁剪，默认为drop_tail.
            drop_tail: 去掉尾部不足一个epoch长度的数据
            no: 不做任何处理
            custom: 自定义，通过tailor_param指定开始时间(sec)和结束时间(sec)来进行裁剪
        :param tailor_type: 目前只支持drop_tail/no/custom
        :param tailor_param: 针对custom方式，指定start_sec/end_sec
        :return:
        """
        if tailor_type == "no":
            return

        start_sec = None
        end_sec = None
        if tailor_type == "drop_tail":
            start_sec = 0
            end_sec = self.seconds // self.epoch_len * self.epoch_len
        if tailor_type == "custom" and tailor_param is not None:
            start_sec = tailor_param['start_sec']
            end_sec = tailor_param['end_sec']
            assert start_sec is not None and end_sec is not None, "tailor_param is a dict consist of start_sec and end_sec, please check!"
        if self.eeg is not None:
            self.eeg = self.eeg[start_sec * self.sf_eeg:end_sec * self.sf_eeg]
            self.eeg_another = self.eeg_another[start_sec * self.sf_eeg:end_sec * self.sf_eeg]
        if self.acc is not None:
            self.acc = self.acc[:, start_sec * self.sf_acc:end_sec * self.sf_acc]
        self.seconds = end_sec - start_sec
        self.start_time = self.start_time + datetime.timedelta(seconds=start_sec)
        self.end_time = self.start_time + datetime.timedelta(seconds=end_sec)
        self.logger.info(
            "Loaded data is clipped to a multiple of the window length, {} total seconds".format(self.seconds))

    def preprocess(self, filter_param={'highpass': 0.5, 'lowpass': None, 'bandstop': [[49, 51]]},
                   tailor_type='drop_tail', tailor_param=None):
        """
        预处理，依次执行裁剪、滤波
        :param filter_param: 滤波参数，包括highpass/lowpass/bandstop三种，bandstop可以有多个带
        :param tailor_type: 裁剪类型
        :param tailor_param: custom裁剪类型中的裁剪参数
        :return:
        """
        if tailor_type is None:
            pass
        else:
            self.tailor_operation(tailor_type, tailor_param)

        self.highpass = filter_param['highpass']
        self.bandstop = filter_param['bandstop']
        self.lowpass = filter_param['lowpass']

        self.eeg = eeg_filter(self.eeg, self.sf_eeg, self.highpass, 3, None, None, self.bandstop, 3)
        self.eeg_another = eeg_filter(self.eeg_another, self.sf_eeg, self.highpass, 3, None, None, self.bandstop, 3)

        log_info = "EEG filtered: "
        if self.highpass is not None:
            log_info += "Highpass: {} Hz".format(self.highpass)
        if self.lowpass is not None:
            log_info += ", Lowpass: {} Hz".format(self.lowpass)
        if self.bandstop is not None:
            log_info += ", Bandstop: {} Hz.".format(self.bandstop)
        self.logger.info(log_info)
        return self

    def wear_detect(self, model_path=None):
        """
        佩戴检测，可以指定模型，未指定则使用内置模型。
        目前内置模型很久未更新，对于X8数据效果不佳，需要重新收集未佩戴数据，重新训练模型。
        :param model_path:
        :return:
        """
        if model_path is not None:
            self.logger.info("Wear detect model is set, please make sure the features are corresponded.")
        person_info = dict(age=30, male=1, datatype=0)
        epochs = self.eeg.shape[0] // (self.sf_eeg * 1)
        input_eeg = self.eeg[0:epochs * self.sf_eeg * 1].reshape(-1, self.sf_eeg)
        wear_detect_features = WearDectectFeature(person_info, input_eeg, self.sf_eeg, context_mode=3).get_features()
        cols_all = wear_detect_features.columns
        cols_eeg = cols_all[cols_all.str.startswith('eeg_')].tolist()
        cols_demo = ['age', 'male', 'data_type']
        features = []
        features = features + cols_eeg
        features = features + cols_demo

        wear_detect_res = wear_detect_with_features(features=wear_detect_features[features], model_path=model_path)

        wear_detect_res = wear_detect_res.reshape([-1, 15])
        wear_detect_res = np.sum(wear_detect_res, axis=1)
        wear_detect_res[wear_detect_res <= 15 * 0.5] = 0
        wear_detect_res[wear_detect_res > 15 * 0.5] = 1

        return wear_detect_res

    def sleep_staging_with_input_model(self, model_path, model_features):
        """
        使用指定path的模型进行分类
        :param model_path: 模型路径
        :param model_features: 用于预测的特征，需要与指定的模型的特征一致
        :return:
        """
        if self.eeg is None:
            self.logger.info("The EEG data is not loaded, please load EEG first.")
        try:
            clf = lgb.Booster(model_file=model_path)
            class_count = clf._Booster__num_class
            assert class_count == len(model_features), "The feature doesn't match the model."
            self.class_count = class_count
            target_feature_name = clf.feature_name()
            target_feature = model_features[target_feature_name]
            assert class_count == len(target_feature), "The feature doesn't match the model."
            self.logger.info("The staging mode is illegal, please check and run again.")
        except Exception as e:
            pass

        self.logger.info("Sleep staging started.")

        self.features = target_feature

        wear_detect_res = self.wear_detect()
        predictions = sleep_staging_with_features(features=self.features, clf=clf)

        if class_count == 5:
            predictions[wear_detect_res == 0] = 5
        elif class_count == 4:
            predictions[wear_detect_res == 0] = 4
        elif class_count == 3:
            predictions[wear_detect_res == 0] = 0

        pp_predictions = pp_label_smooth(np.copy(predictions), window=2)
        self.sleep_staging_result = pp_predictions
        self.logger.info("Sleep staging finished.")

        return self

    def sleep_staging_with_internal_model(self, use_acc=False, use_time=False, staging_mode='offline'):
        """
        指定内置模型用于睡眠分期：
        1. use_acc/use_time/context_mode/class_count为一组，设置后会自动寻找符合要求的内置模型进行分期
        2. model_path为一组，指定自定义的
        :param use_acc: 使用体动特征
        :param use_time: 使用时间特征
        :param staging_mode: 分期模式/上下文特征。'realtime'：实时模式，只用上文特征；2：'offline'：非实时模式，用上下文特征
        :return:
        """
        if self.eeg is None:
            self.logger.info("The EEG data is not loaded, please load EEG first.")
        if staging_mode not in ['offline', 'realtime']:
            self.logger.info("The staging mode is illegal, please check and run again.")
        self.logger.info("Sleep staging started.")
        self.staging_mode = staging_mode
        if self.staging_mode == 'realtime':
            context_mode = 1
        elif self.staging_mode == 'offline':
            context_mode = 2
        epochs = self.eeg.shape[0] // (self.sf_eeg * self.epoch_len)
        input_eeg = self.eeg[0:epochs * self.sf_eeg * self.epoch_len].reshape(-1, self.sf_eeg * self.epoch_len)

        input_acc = None
        if use_acc and self.acc is not None:
            acc = self.acc[:, 0:epochs * self.sf_acc * self.epoch_len]
            # acc = data['acc']
            accx = acc[0, :].reshape(-1, 1, 750)
            accy = acc[1, :].reshape(-1, 1, 750)
            accz = acc[2, :].reshape(-1, 1, 750)
            input_acc = np.concatenate([accx, accy, accz], axis=1)

        self.features = RSCFeature(self.features['meta'], raw_eeg=input_eeg, raw_acc=input_acc,
                                   sf_eeg=self.sf_eeg, sf_acc=self.sf_acc, context_mode=context_mode).get_features()
        self.logger.info("Feature extraction finished.")
        wear_detect_res = self.wear_detect()

        clf = load_model(use_acc=use_acc, use_time=use_time, context_mode=context_mode)
        class_count = clf._Booster__num_class
        self.class_count = class_count
        predictions = sleep_staging_with_features(features=self.features, clf=clf)
        #
        self.logger.info("Predicting sleep outcomes...ing, may cost 20 min")
        predictions_with_sleepyco_net = predict_with_raw_eeg(self.raw_eeg, 500)  # 使用raw_eeg和sleepyco预测睡眠结果
        if len(predictions_with_sleepyco_net) < len(predictions):
            predictions_with_sleepyco_net = np.pad(predictions_with_sleepyco_net, (0, len(predictions) - len(predictions_with_sleepyco_net)), 'constant', constant_values=(predictions_with_sleepyco_net[-1]))
        predictions = predictions_with_sleepyco_net
        #
        if class_count == 5:
            predictions[wear_detect_res == 0] = 5
        elif class_count == 4:
            predictions[wear_detect_res == 0] = 4

        pp_predictions = pp_label_smooth(np.copy(predictions), window=2)
        self.sleep_staging_result = pp_predictions
        self.logger.info("Sleep staging finished.")

        return self

    def plot_sleep_data(self, plot_spectral=True, plot_acc=True, plot_staging=True, plot_variables=True, savefig=None):
        """
        绘制睡眠分析图，包括：
        1. 时频图
        2. 体动差分图
        3. 睡眠姿势图
        4. 睡眠分期图：模型的分类数会影响睡眠分期图的样式
        5. 睡眠指标（标注在睡眠分期图中）
        :param plot_spectral: 是否绘制时频图
        :param plot_acc: 是否绘制体动数据，包括体动差分和睡眠姿势
        :param plot_staging: 是否绘制睡眠分期图
        :param plot_variables: 是否绘制睡眠指标
        :param savefig: 图片保存路径
        :return:
        """
        if self.sleep_staging_result is None or self.class_count is None:
            self.logger.info("Sleep staging result is none, auto sleep staging will run first!")
        if self.acc is None:
            plot_acc = False
            self.logger.info("The ACC is not loaded, ACC plot will be skipped.")
        if plot_variables and self.sleep_variables is None:
            self.logger.info(
                "Sleep variables is none, and will computed first. If you don't want it, just change \"plot_variables\" to False.")
            self.compute_sleep_variables()

        subplot_count = 0 + 2 * plot_acc + plot_spectral + plot_staging
        fig_height = subplot_count * 4 + (1 if plot_spectral else 0)
        height_ratio = (np.ones(subplot_count) * 4).tolist()
        if plot_spectral:
            height_ratio[0] = 5.0
        # fig, ax = plt.subplots(subplot_count, 1, figsize=(16, fig_height), height_ratio=height_ratio)
        fig = plt.figure(figsize=(20, fig_height))
        gs = gridspec.GridSpec(subplot_count, 1, height_ratios=height_ratio)
        # fig.subplots_adjust(hspace=0.5)
        # if subplot_count == 1:
        #     ax = [ax]

        i = 0
        if plot_spectral:
            ax_1 = fig.add_subplot(gs[i, 0])
            plot_spectrogram(fig, ax_1, self.eeg, self.start_time, self.sf_eeg)
            i += 1
        if plot_acc:
            ax_2 = fig.add_subplot(gs[i, 0])
            plot_avg_diff_acc(fig, ax_2, self.acc, self.start_time, self.sf_acc)
            i += 1
            if self.sleep_postures is None:
                self.sleep_postures = sleep_posture_analyse(self.acc)
            ax_3 = fig.add_subplot(gs[i, 0])
            plot_sleep_posture(fig, ax_3, self.sleep_postures, self.start_time, self.sf_acc)
            i += 1
        if plot_staging:
            if self.sleep_staging_result is None:
                self.logger.info("The sleep staging result is None, auto sleep staging will run first!")
                self.sleep_staging_with_internal_model()
            variables = None
            if plot_variables:
                variables = self.sleep_variables
                if variables is None:
                    self.logger.info("The sleep variables is None, sleep variables will be computed first.")
                    self.compute_sleep_variables()
                    variables = self.sleep_variables
            ax_4 = fig.add_subplot(gs[i, 0])
            if self.class_count == 5:
                plot_sleep_staging_result_5c(fig, ax_4, self.sleep_staging_result, variables, self.start_time)
            elif self.class_count == 4:
                plot_sleep_staging_result_4c(fig, ax_4, self.sleep_staging_result, variables, self.start_time)
        plt.tight_layout()
        if savefig is not None:
            plt.savefig(savefig, dpi=300, bbox_inches='tight')
            self.analysis_fig_path = savefig
            self.logger.info("The sleep data plot is saved as {}".format(savefig))
        return self

    def plot_data_preview(self, plot_spectral=True, plot_acc=True, savefig=None):
        # 绘制小鼠data_preview
        subplot_count = 0 + 1 * plot_acc + 2 * plot_spectral
        fig_height = subplot_count * 4 + (2 if plot_spectral else 0)
        height_ratio = (np.ones(subplot_count) * 4).tolist()
        if plot_spectral:
            height_ratio[0] = 5.0
            height_ratio[1] = 5.0
        # fig, ax = plt.subplots(subplot_count, 1, figsize=(16, fig_height), height_ratio=height_ratio)
        fig = plt.figure(figsize=(20, fig_height))
        gs = gridspec.GridSpec(subplot_count, 1, height_ratios=height_ratio)
        # fig.subplots_adjust(hspace=0.5)
        # if subplot_count == 1:
        #     ax = [ax]

        i = 0
        if plot_spectral:
            ax_1 = fig.add_subplot(gs[i, 0])
            plot_spectrogram(fig, ax_1, self.eeg, self.start_time, self.sf_eeg)
            i += 1
        if plot_spectral:
            ax_2 = fig.add_subplot(gs[i, 0])
            plot_spectrogram(fig, ax_2, self.eeg_another, self.start_time, self.sf_eeg)
            i += 1
        if plot_acc:
            ax_3 = fig.add_subplot(gs[i, 0])
            plot_avg_diff_acc(fig, ax_3, self.acc, self.start_time, self.sf_acc)
            i += 1
        plt.tight_layout()
        if savefig is not None:
            plt.savefig(savefig, dpi=300, bbox_inches='tight')
            self.data_preview_fig_path = savefig
            self.logger.info("The sleep data plot is saved as {}".format(savefig))
        return self

    def plot_anes_data(self, plot_spectral=True, plot_acc=True, plot_staging=True, plot_variables=False, savefig=None):
        """
        绘制麻醉数据图，包括：
        1. 时频图
        2. 体动差分图
        3. 睡眠姿势图
        4. 麻醉深度图：麻醉深度指数随时间变化，将麻醉深度粗略分为5类
        :param plot_spectral: 是否绘制时频图
        :param plot_acc: 是否绘制体动数据，包括体动差分和睡眠姿势
        :param plot_staging: 是否绘制麻醉深度
        :param plot_variables: 是否绘制睡眠指标（麻醉场景不适用，设为False）
        :param savefig: 图片保存路径
        :return:
        """
        if self.sleep_staging_result is None:
            self.logger.info("Sleep staging result is none, auto sleep staging will run first!")
        if self.acc is None:
            plot_acc = False
            self.logger.info("The ACC is not loaded, ACC plot will be skipped.")
        if plot_variables and self.sleep_variables is None:
            self.logger.info(
                "Sleep variables is none, and will computed first. If you don't want it, just change \"plot_variables\" to False.")
            self.compute_sleep_variables()

        subplot_count = 0 + 2 * plot_acc + plot_spectral + plot_staging
        fig_height = subplot_count * 4 + (1 if plot_spectral else 0)
        height_ratio = (np.ones(subplot_count) * 4).tolist()
        if plot_spectral:
            height_ratio[0] = 5.0
        # fig, ax = plt.subplots(subplot_count, 1, figsize=(16, fig_height), height_ratio=height_ratio)
        fig = plt.figure(figsize=(20, fig_height))
        gs = gridspec.GridSpec(subplot_count, 1, height_ratios=height_ratio)
        # fig.subplots_adjust(hspace=0.5)
        # if subplot_count == 1:
        #     ax = [ax]

        i = 0
        if plot_spectral:
            ax_1 = fig.add_subplot(gs[i, 0])
            plot_spectrogram(fig, ax_1, self.eeg, self.start_time, self.sf_eeg, vmin=-20)
            i += 1
        if plot_acc:
            ax_2 = fig.add_subplot(gs[i, 0])
            plot_avg_diff_acc(fig, ax_2, self.acc, self.start_time, self.sf_acc)
            i += 1
            if self.sleep_postures is None:
                self.sleep_postures = sleep_posture_analyse(self.acc)
            ax_3 = fig.add_subplot(gs[i, 0])
            plot_sleep_posture(fig, ax_3, self.sleep_postures, self.start_time, self.sf_acc)
            i += 1
        if plot_staging:
            if self.sleep_staging_result is None:
                self.logger.info("The sleep staging result is None, auto sleep staging will run first!")
                self.sleep_staging_with_internal_model()
            variables = None
            if plot_variables:
                variables = self.sleep_variables
                if variables is None:
                    self.logger.info("The sleep variables is None, sleep variables will be computed first.")
                    self.compute_sleep_variables()
                    variables = self.sleep_variables
            ax_4 = fig.add_subplot(gs[i, 0])
            plot_sleep_staging_result_5c(fig, ax_4, self.sleep_staging_result, variables, self.start_time)
        plt.tight_layout()
        if savefig is not None:
            plt.savefig(savefig, dpi=300, bbox_inches='tight')
            self.analysis_fig_path = savefig
            self.logger.info("The sleep data plot is saved as {}".format(savefig))
        return self

    def compute_sleep_variables(self, hypno=None):
        """
        根据睡眠分期结果，计算相关睡眠指标。
        除了加载澜猫数据，进行分期，再根据分期结果计算睡眠指标之外，还可以通过load_hypno方法加载人工分期等，再通过当前方法计算睡眠指标。
        计算的指标包括：
        TRT：总记录时间
        TST：总睡眠时间
        SOL：睡眠延迟
        GU：起床时间
        WASO/ART：睡中觉醒时间
        SE：睡眠效率
        AR：睡中觉醒次数

        :param hypno: 额外指定的睡眠分期结果，一维ndarray数组。为None时表示使用data handler里的睡眠分期结果
        :return:
        """
        if hypno is not None:
            self.logger.info("Sleep variables will be computed by the giving hypno instead of the loaded data!")
        else:
            if self.sleep_staging_result is None:
                self.logger.info(
                    "Sleep variables are based on sleep staging result, auto sleep staging will run first!")
                self.sleep_staging_with_internal_model()
            hypno = np.copy(self.sleep_staging_result)

        if self.class_count == 5:
            be = (np.where(hypno == 5)[0].size) / hypno.shape[0]
        elif self.class_count == 4:
            be = (np.where(hypno == 4)[0].size) / hypno.shape[0]
        trt = hypno.shape[0] * self.epoch_len
        tst = tst_compute(hypno, self.class_count, self.epoch_len)
        sl = sl_compute(hypno, self.class_count, self.epoch_len)
        # tc = turnover_count(acc=self.acc, hypno=hypno)
        if sl == -1:
            self.logger.info("No continuous sleep epochs are detected!")
            se = 0.0
            arousal_time = np.asarray([])
            arousal_count = 0
            waso = 0
            gu = -1
        else:
            gu = get_up_time_compute(hypno, self.class_count, self.epoch_len)
            se = se_compute(hypno, self.class_count)
            arousal_count, arousal_time = arousal_time_compute(hypno, self.class_count, self.epoch_len,
                                                               sleep_range=[sl, gu])
            waso = arousal_time.shape[0] * self.epoch_len

        if sl >= 0 and gu >= 0 and gu + sl <= hypno.shape[0] * 15:
            sl_index = sl // 15
            gu_index = (hypno.shape[0] - gu // 15)
            sleep_hypno = hypno[sl_index: gu_index]
            rem_hypno = np.where(sleep_hypno == 3)[0].shape[0] * 15
            n12_hypno = np.union1d(np.where(sleep_hypno == 1)[0], np.where(sleep_hypno == 2)[0]).shape[0] * 15
            n3_hypno = np.where(sleep_hypno == 0)[0].shape[0] * 15
        else:
            rem_hypno = -1
            n12_hypno = -1
            n3_hypno = -1
        self.sleep_variables = {
            "TRT": trt,
            "TST": tst,
            "SOL": sl,
            "GU": gu,
            "WASO": waso,
            "SE": se,
            "AR": arousal_count,
            "ART": arousal_time,
            "N3": n3_hypno,
            "N12": n12_hypno,
            "REM": rem_hypno,
            "BE": be,
            "HYPNO": str(hypno.tolist())
        }
        print(
            "TST:\t{} s\nSOL:\t{} s\nSE:\t\t{}%\nWASO:\t{} s\nAR:\t\t{}".format(tst, sl, se * 100, waso, arousal_count))

        return self

    def get_sleep_variables(self):
        """
        获取睡眠变量
        :return:
        """
        if self.sleep_variables is None:
            self.logger.error("Sleep variables are None, please run compute_sleep_variables first.")
        return self.sleep_variables

    def spindle_detect(self, hypno_mask=(0, 1), freq_sp=(12, 15), freq_broad=(1, 30), duration=(0.5, 2),
                       min_distance=100,
                       thresh_rel_pow=0.15, thresh_corr=0.60, thresh_rms=1.5):
        """
        Spindle检测：对已加载的脑电信号进行Spindle检测，代码来自Yasa，默认参数做了调整，代码流程根据澜猫数据做了适配修改
        检测结果保存成DataFrame形式，每个Spindle会记录其范围、特征值等信息
        :param hypno_mask: 表示在哪些睡眠阶段进行检测，需要已经完成睡眠分期。
        :param freq_sp: Spindle的频率范围
        :param freq_broad: 频谱范围
        :param duration: 持续时长
        :param min_distance: 两个Spindle之间的最短距离
        :param thresh_rel_pow: 核心参数1
        :param thresh_corr: 核心参数2
        :param thresh_rms: 核心参数3
        :return:
        """
        self.logger.info("Spindle detect start.")

        mask = None
        if hypno_mask is not None:
            if self.sleep_staging_result is None:
                self.logger.info(
                    "Sleep staging result is need for spindle detection, auto sleep staging will run first!")
                self.sleep_staging_with_internal_model()
            mask = np.in1d(self.sleep_staging_result, hypno_mask)
            mask = np.repeat(mask, self.sf_eeg * self.epoch_len)

        self.sp_df = spindles_detect(self.eeg, mask=mask, freq_sp=freq_sp, freq_broad=freq_broad,
                                     duration=duration,
                                     min_distance=min_distance, thresh_rel_pow=thresh_rel_pow, thresh_rms=thresh_rms,
                                     thresh_corr=thresh_corr)
        logging.getLogger("").isEnabledFor(logging.WARNING)

        if self.sleep_staging_result is not None:
            n12_set = set(np.where(self.sleep_staging_result == 1)[0])
            n3_set = set(np.where(self.sleep_staging_result == 0)[0])
            sp_end_epoch = self.sp_df["End_Index"].to_numpy() // (15 * 500)

            n12_sp_count = len(np.where(np.in1d(sp_end_epoch, np.array(list(n12_set))) == True)[0])
            n3_sp_count = len(np.where(np.in1d(sp_end_epoch, np.array(list(n3_set))) == True)[0])

            self.sleep_variables["n12_sp_count"] = n12_sp_count
            self.sleep_variables["n3_sp_count"] = n3_sp_count
        if self.biomarker is None:
            self.biomarker = np.zeros(self.eeg.shape[0])
        for row in np.arange(self.sp_df.shape[0]):
            self.biomarker[self.sp_df['Start_Index'][row]:self.sp_df['End_Index'][row]] = 1
        self.logger.info("Spindle detect finished.")
        # print(self.sp_df)
        return self

    def sw_detect(self, hypno_mask=(0, 1), freq_sw=(0.3, 1.5), dur_neg=(0.3, 1.2), dur_pos=(0.3, 1.5),
                  amp_neg=(20, 300),
                  amp_pos=(15, 300), amp_ptp=(45, 600), coupling=False, coupling_params=None):
        """
        慢波检测：对已经加载的脑电信号进行慢波检测，代码来自Yasa，默认参数做了调整，代码流程根据澜猫数据做了适配修改
        检测结果保存成DataFrame形式，每个慢波会记录其范围、特征值等信息
        :param hypno_mask: 表示在哪些睡眠阶段进行检测，需要已经完成睡眠分期。
        :param freq_sw: 慢波的频率
        :param dur_neg: 负半波持续时间
        :param dur_pos: 正半波持续时间
        :param amp_neg: 负半波峰值
        :param amp_pos: 正半波峰值
        :param amp_ptp: 峰峰值
        :param coupling: Yasa原有参数，不明
        :param coupling_params: Yasa原有参数，不明
        :return:
        """
        self.logger.info("Slow-wave detect start.")
        mask = None
        if hypno_mask is not None:
            if self.sleep_staging_result is None:
                self.logger.info(
                    "Sleep staging result is need for slow-wave detection, auto sleep staging will run first!")
                self.sleep_staging_with_internal_model()
            mask = np.in1d(self.sleep_staging_result, hypno_mask)
            mask = np.repeat(mask, self.sf_eeg * self.epoch_len)

        self.sw_df = sw_detect(self.eeg, sf=self.sf_eeg, mask=mask, freq_sw=freq_sw, dur_neg=dur_neg,
                               dur_pos=dur_pos,
                               amp_neg=amp_neg, amp_pos=amp_pos, amp_ptp=amp_ptp, coupling=coupling,
                               coupling_params=coupling_params)

        if self.sleep_staging_result is not None:
            n12_set = set(np.where(self.sleep_staging_result == 1)[0])
            n3_set = set(np.where(self.sleep_staging_result == 0)[0])
            sw_end_epoch = self.sw_df["End_Index"].to_numpy() // (15 * 500)

            n12_sw_count = len(np.where(np.in1d(sw_end_epoch, np.array(list(n12_set))) == True)[0])
            n3_sw_count = len(np.where(np.in1d(sw_end_epoch, np.array(list(n3_set))) == True)[0])

            self.sleep_variables["n12_sw_count"] = n12_sw_count
            self.sleep_variables["n3_sw_count"] = n3_sw_count
        if self.biomarker is None:
            self.biomarker = np.zeros(self.eeg.shape[0])
        for row in np.arange(self.sw_df.shape[0]):
            self.biomarker[self.sw_df['Start_Index'][row]:self.sw_df['End_Index'][row]] = 2
        self.logger.info("Slow-wave detect finished.")
        # print(self.sw_df)
        return self

    def export_sp_results(self, save_file=None):
        """
        导出Spindle检测结果到Excel文件中
        :param save_file: Excel文件保存路径
        :return:
        """
        if self.sp_df is None:
            self.logger.info("The spindle detection result is None, spindle detection will run first.")
            self.spindle_detect()
        if save_file is None:
            self.logger.info("File save path is not configured, default saved to ./saved_files/{}".format(
                "spindle_result_" + self.data_name + ".csv"))
            if not os.path.exists("../saved_file"):
                os.mkdir("../saved_file")
            self.sp_df.to_csv("./saved_file/" + "spindle_result_" + self.data_name + ".csv")
        else:
            self.sp_df.to_csv(save_file)
            self.logger.info("Save file to {}.".format(save_file))

        return self

    def export_sw_results(self, save_file=None):
        """
        导出慢波检测结果到Excel文件中
        :param save_file: Excel文件保存路径
        :return:
        """
        if self.sw_df is None:
            self.logger.info("The slow-wave detection result is None, slow-wave detection will run first.")
            self.sw_detect()
        if save_file is None:
            self.logger.info("File save path is not configured, default saved to ./saved_files/{}".format(
                "slow_wave_result_" + self.data_name + ".csv"))
            if not os.path.exists("../saved_file"):
                os.mkdir("../saved_file")
            self.sw_df.to_csv("./saved_file/" + "slow_wave_result_" + self.data_name + ".csv")
        else:
            self.sw_df.to_csv(save_file)
            self.logger.info("Save file to {}.".format(save_file))
        return self

    def plot_sp_results_by_id(self, sp_index, range=5000, savefig=None):
        """
        根据Spindle检测的结果，指定Spindle的编号，绘制Spindle图形
        :param sp_index: Spindle编号，最小为1
        :param range: 以指定Spindle为中心，整张图片的总点数，默认为5000，最大不超过8000
        :param savefig: 图片保存路径
        :return:
        """
        if self.sp_df is None:
            self.logger.info("You have not run spindle detect, spindle detect will run first!")
            self.spindle_detect()
        if self.sp_df.size < sp_index or sp_index <= 0:
            self.logger.error("The input sp_index is invalid, please check!")
        sp = self.sp_df.iloc[sp_index]
        mid = (sp["Start_Index"] + sp["End_Index"]) // 2
        min_index = max(mid - range / 2, 0)
        max_index = min(mid + range / 2, self.eeg.shape[0])
        self.plot_sp_results_by_range(start_index=min_index, end_index=max_index,
                                      title="spindle detection result: No.{}".format(sp_index), savefig=savefig)
        if savefig is not None:
            self.logger.info("The spindle plot is saved to {}".format(savefig))
        return self

    def plot_sp_results_by_range(self, start_index, end_index, title=None, savefig=None):
        """
        指定脑电信号的范围，绘制该范围里的脑电信号，范围里面的Spindle会进行红色标记
        :param start_index: 起始点下标
        :param end_index: 终止点下标
        :param title: 图片标题
        :param savefig: 图片保存路径
        :return:
        """
        if end_index - start_index > 8000:
            self.logger.error("For best view, please make sure the sample size is around 5000, plot is skipped.")
            return
        if self.sp_df is None:
            self.logger.info("You have not run spindle detect, spindle detect will run first!")
            self.spindle_detect()
        start_index = int(start_index)
        end_index = int(end_index)
        mask = self.biomarker[start_index: end_index]
        data = self.eeg[start_index: end_index]
        mask[mask != 1] = np.nan
        times = np.arange(start_index, end_index) / self.sf_eeg
        plt.figure(figsize=(14, 4))
        plt.plot(times, data, 'k')
        plt.plot(times, mask * data, 'indianred')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude (uV)')
        plt.xlim([times[0], times[-1]])
        if title is None:
            plt.title(
                "spindle detect result between [{}s, {}s]".format(start_index / self.sf_eeg, end_index / self.sf_eeg))
        else:
            plt.title(title)
        sns.despine()
        if savefig is not None:
            plt.savefig(savefig, dpi=300, bbox_inches='tight')
        return self

    def plot_sw_results_by_id(self, sw_index, range=5000, savefig=None):
        """
        根据慢波检测的结果，指定慢波的编号，绘制慢波图形
        :param sw_index: 指定的慢波编号
        :param range: 以指定的慢波为中心，待绘制的脑电信号点数（宽度）
        :param savefig: 图片待保存路径
        :return:
        """
        if self.sw_df is None:
            self.logger.info("You have not run slow wave detect, slow wave detect will run first!")
            self.sw_detect()
        if self.sw_df.size < sw_index or sw_index <= 0:
            self.logger.error("The input sp_index is invalid, please check!")
        sw = self.sw_df.iloc[sw_index]
        mid = (sw["Start_Index"] + sw["End_Index"]) // 2
        min_index = max(mid - range / 2, 0)
        max_index = min(mid + range / 2, self.eeg.shape[0])
        self.plot_sw_results_by_range(start_index=min_index, end_index=max_index,
                                      title="slow wave result: No.{}".format(sw_index), savefig=savefig)
        if savefig is not None:
            self.logger.info("The slow-wave plot is saved as {}".format(savefig))
        return self

    def plot_sw_results_by_range(self, start_index, end_index, title=None, savefig=None):
        """
        指定脑电信号的范围，绘制该范围里的脑电信号，范围里面的慢波会进行红色标记
        :param start_index: 起始点下标
        :param end_index: 终止点下标
        :param title: 图片标题
        :param savefig: 图片待保存路径
        :return:
        """
        if self.sw_df is None:
            self.logger.info("You have not run slow wave detect, slow wave detect will run first!")
            self.sw_detect()

        if end_index - start_index > 8000:
            self.logger.error("For best view, please make sure the sample size is around 5000!")
            return
        start_index = int(start_index)
        end_index = int(end_index)
        mask = self.biomarker[start_index: end_index]
        data = self.eeg[start_index: end_index]
        mask[mask != 2] = np.nan
        mask[mask == 2] = 1
        times = np.arange(start_index, end_index) / self.sf_eeg
        plt.figure(figsize=(14, 4))
        plt.plot(times, data, 'k')
        plt.plot(times, mask * data, 'indianred')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude (uV)')
        plt.xlim([times[0], times[-1]])
        if title is None:
            plt.title("slow wave result between [{}s, {}s]".format(start_index / self.sf_eeg, end_index / self.sf_eeg))
        else:
            plt.title(title)
        sns.despine()
        if savefig is not None:
            plt.savefig(savefig, dpi=300, bbox_inches='tight')
        return self

    def plot_sw_stim_sham(self, savefig=None):
        """
        绘制慢波增强刺激对比图
        :param savefig: 图片待保存路径
        :return:
        """
        if self.raw_sti is None or len(self.raw_sti.shape) == 0:
            self.logger.error(
                "The sti indexs is None, please make sure the .sti file is loaded before plot sw stim vs sham.")
            return self
        if self.raw_sti.shape[0] < 10:
            self.logger.error(
                "The count of stim/sham points is less than expected, slow-wave stim sham plot will be skipped.")
            return self
        eeg_copy = np.copy(self.raw_eeg)
        plot_stim_sham_sw(self.device_type, eeg_copy, self.start_time, self.raw_sti, self.sf_eeg, savefig)

    def export_analysis_result_to_xlsx(self, save_path, sw_results=True, sp_results=True, sleep_variables=True):
        """
        导出睡眠分析结果（可以包含睡眠分期、睡眠变量、慢波检测、Spindle检测）到Excel中
        :param save_path: Excel保存路径
        :param sw_results: 慢波检测结果
        :param sp_results: Spindle检测结果
        :param sleep_variables: 睡眠变量
        :return:
        """
        if save_path is None:
            self.logger.warning("Analysis results save path is None, xlsx file will not be saved, please check.")
            return self
        sheet_count = 0
        df_sw = df_sp = df_sv = None
        if sw_results:
            df_sw = self.sw_df
            sheet_count += 1

        if sp_results:
            df_sp = self.sp_df
            sheet_count += 1

        if sleep_variables:
            sleep_variables_df = {
                "data_name": [self.data_name],
                "TST(H)": [self.sleep_variables["TST"] / 3600],
                "SOL(H)": [self.sleep_variables["SOL"] / 3600],
                "GU(H)": [self.sleep_variables["GU"] / 3600],
                "WASO(M)": [self.sleep_variables["WASO"] / 60],
                "SE(%)": [self.sleep_variables["SE"] * 100],
                "AR": [self.sleep_variables["AR"]],
                "N3(H)": [self.sleep_variables["N3"] / 3600],
                "N12(H)": [self.sleep_variables["N12"] / 3600],
                "REM(H)": [self.sleep_variables["REM"] / 3600],
                "SW": [self.sw_df.shape[0]] if self.sw_df is not None else None,
                "N3_SW_Count": [self.sleep_variables["n3_sw_count"]] if self.sleep_variables.__contains__(
                    "n3_sw_count") else None,
                "N12_SW_Count": [self.sleep_variables["n12_sw_count"]] if self.sleep_variables.__contains__(
                    "n12_sw_count") else None,
                "SP": [self.sp_df.shape[0]] if self.sp_df is not None else None,
                "N3_SP_Count": [self.sleep_variables["n3_sp_count"]] if self.sleep_variables.__contains__(
                    "n3_sp_count") else None,
                "N12_SP_Count": [self.sleep_variables["n12_sp_count"]] if self.sleep_variables.__contains__(
                    "n12_sp_count") else None,
                "Sti_Count": [
                    self.raw_sti.shape[0] // 2 if (self.raw_sti is not None and len(self.raw_sti.shape) != 0) else 0],
                "Hypno": [self.sleep_variables["HYPNO"]]
            }

            df_sv = pd.DataFrame(sleep_variables_df)
            sheet_count += 1
        if sheet_count == 0:
            self.logger.info("At least one sheet is needed to export analysis result xlsx.")
            return self

        with pd.ExcelWriter(save_path) as writer:
            if df_sw is not None:
                df_sw.to_excel(writer, sheet_name='slow-wave results')
            else:
                self.logger.warning("Slow-wave detect result is None, please make sure slow-wave detection is done.")
            if df_sp is not None:
                df_sp.to_excel(writer, sheet_name='spindle results')
            else:
                self.logger.warning("Spindle detect result is None, please make sure spindle detection is done.")
            if df_sv is not None:
                df_sv.to_excel(writer, sheet_name='sleep variables')
            else:
                self.logger.warning("Sleep variables result is None, please make sure sleep variable is computed.")
        # savemat(save_path.replace("analysis_results.xlsx", "prediction_0.85.mat"),
        #         {"prediction": self.sleep_staging_result})
        return self

    def show_plots(self):
        """
        显示结果图片
        :return:
        """
        plt.show()

    def export_analysis_report(self, pdf_save_path):
        """
        导出睡眠分析结果成PDF，包括各项睡眠指标、睡眠分析图和数据基本信息
        :param pdf_save_path: PDF保存路径
        :return:
        """
        content = {}
        if self.analysis_fig_path is None or not os.path.exists(self.analysis_fig_path):
            self.logger.error("The sleep data figure not exists, the responding area will be blank in the pdf file.")
        else:
            content["sleep_plot"] = self.analysis_fig_path

        if self.patient_info is None:
            self.logger.error("The patient info not exists, the responding area will be blank in the pdf file.")
        else:
            content["phone_number"] = self.patient_info["phone_number"]
            if self.patient_info.__contains__("name"):
                content["name"] = self.patient_info["name"]

        if self.record_info is None:
            self.logger.error("The record info not exists, the responding area will be blank in the pdf file.")
        else:
            content["record_date"] = self.record_info["record_date"]
            content["record_start_time"] = self.record_info["record_start_time"][0:19]
            content["record_end_time"] = self.record_info["record_end_time"][0:19]

        if self.package_loss_rate is None:
            self.logger.error("The package loss rate not exists, the responding area will be blank in the pdf file.")
        else:
            content["package_loss_rate"] = "{:.2f}%".format(self.package_loss_rate)

        if self.disconnect_rate is None:
            self.logger.error("The disconnection rate not exists, the responding area will be blank in the pdf file.")
        else:
            content["disconnection_rate"] = "{:.2f}%".format(self.disconnect_rate)

        if self.sleep_variables is None:
            self.logger.error("The sleep variables not exist, the responding area will be blank in the pdf file.")
        else:
            content["trt"] = self.sleep_variables["TRT"] / 60
            content["tst"] = self.sleep_variables["TST"] / 60
            content["sl"] = self.sleep_variables["SOL"] / 60
            content["waso"] = self.sleep_variables["WASO"] / 60
            content["ar"] = self.sleep_variables["AR"]
            content["se"] = "{:.2f}%".format(self.sleep_variables["SE"] * 100)
            content["N1/N2"] = self.sleep_variables["N12"] / 60
            content["N3"] = self.sleep_variables["N3"] / 60
            content["REM"] = self.sleep_variables["REM"] / 60

        if pdf_save_path is None:
            self.logger.info("The pdf save path is not configured, pdf will be saved with raw data.")
            pdf_save_path = os.path.join(self.data_path, "sleep_report.pdf")
        report_pdf_generator(pdf_save_path, content)

    def export_data_preview(self, pdf_save_path):

        content = {}
        if self.data_preview_fig_path is None or not os.path.exists(self.data_preview_fig_path):
            self.logger.error("The sleep data figure not exists, the responding area will be blank in the pdf file.")
        else:
            content["sleep_plot"] = self.data_preview_fig_path

        if self.patient_info is None:
            self.logger.error("The patient info not exists, the responding area will be blank in the pdf file.")
        else:
            content["phone_number"] = self.patient_info["phone_number"]
            if self.patient_info.__contains__("name"):
                content["name"] = self.patient_info["name"]

        if self.record_info is None:
            self.logger.error("The record info not exists, the responding area will be blank in the pdf file.")
        else:
            content["record_date"] = self.record_info["record_date"]
            content["record_start_time"] = self.record_info["record_start_time"][0:19]
            content["record_end_time"] = self.record_info["record_end_time"][0:19]

        if self.package_loss_rate is None:
            self.logger.error("The package loss rate not exists, the responding area will be blank in the pdf file.")
        else:
            content["package_loss_rate"] = "{:.2f}%".format(self.package_loss_rate)

        if self.disconnect_rate is None:
            self.logger.error("The disconnection rate not exists, the responding area will be blank in the pdf file.")
        else:
            content["disconnection_rate"] = "{:.2f}%".format(self.disconnect_rate)

        if self.sleep_variables is None:
            self.logger.error("The sleep variables not exist, the responding area will be blank in the pdf file.")
        else:
            content["trt"] = self.sleep_variables["TRT"] / 60
            content["tst"] = self.sleep_variables["TST"] / 60
            content["sl"] = self.sleep_variables["SOL"] / 60
            content["waso"] = self.sleep_variables["WASO"] / 60
            content["ar"] = self.sleep_variables["AR"]
            content["se"] = "{:.2f}%".format(self.sleep_variables["SE"] * 100)
            content["N1/N2"] = self.sleep_variables["N12"] / 60
            content["N3"] = self.sleep_variables["N3"] / 60
            content["REM"] = self.sleep_variables["REM"] / 60

        if pdf_save_path is None:
            self.logger.info("The pdf save path is not configured, pdf will be saved with raw data.")
            pdf_save_path = os.path.join(self.data_path, "sleep_report.pdf")
        gen_pdf_ar4(pdf_save_path, content)
