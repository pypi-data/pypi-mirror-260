import os.path
import sys
import numpy as np
import lightgbm as lgb
import scipy.signal as sp_sig
from scipy import signal
from scipy.integrate._quadrature import simps
from scipy.io import loadmat

from lmsleepdata.data_download.data_download import download_lm_data_from_server
from lmsleepdata.datahandler import DataHandler
import pandas as pd

from lmsleepdata.function_in_test.other_features import generate_cluster_feature1, generate_cluster_feature2, \
    generate_cluster_feature3
from lmsleepdata.scripts.script_functions import local_datas_full_analyse

if __name__ == '__main__':
    start_day = '20231130'
    end_day = '20231130'
    download_param = {
        # 正式服：http://8.136.42.241/， 测试服：http://150.158.153.12/
        'url': 'http://8.136.42.241:38083/inner/filter',
        # 刺激范式：1. 手动刺激，2. 音频刺激，3. N3闭环刺激，4. 纯记录模式，5. 记录模式， 6. 音频刺激
        'paradigms': None,
        # 用户手机号
        'phones': [15777799719],
        # 基座mac
        'macs': None,
        # 服务版本
        'serviceVersions': None,
        # 睡眠主观评分，1~5，-1表示未评分
        'sleepScores': None,
        # 停止类型， 0. 断连超时, 1. 用户手动, 2. 头贴放到基座上停止, 3. 关机指令触发, 4. 低电量, 5. 崩溃
        'stopTypes': None,
        # 时间范围，以停止记录的时间为准
        'dateRange': [str(start_day), str(end_day)],
        # 数据时长范围
        'dataLengthRange': [60 * 3 * 60, 60 * 12 * 60],
        # 翻身次数范围
        'turnoverCountRange': None,
        # 刺激次数范围
        'stimulationCountRange': None,
        # 下载保存路径
        'save_path': os.path.join('E:/dataset/x7_tail', "{}_{}".format(start_day, end_day)),
        # 分析结果保存路径（为None表示保存在数据下载路径中）
        'analysis_save_path': os.path.join('E:/dataset/x7_tail', "{}_{}".format(start_day, end_day)),
    }
    analyse_param = {
        # 设备类型：X7/X8
        'device_type': "X8",
        # 数据类型：sleep(睡眠数据) / anes(麻醉数据)
        'data_type': "sleep",
        # 滤波参数，一般不需要改动
        'pre_process_param': {'highpass': 0.5, 'lowpass': None, 'bandstop': [[49, 51]]},
        # 分期参数：1.是否使用体动特征；2.是否使用时间特征；3.分期模式（实时/非实时）
        'sleep_staging_param': {'use_acc': False, 'use_time': False, 'staging_mode': 'offline'},
        # 是否额外保存数据成.mat格式
        'parse_to_mat': True,
        # 是否额外保存特征到.parquet格式
        'save_features': True,
        # 是否进行慢波检测
        'slow_wave_detect': False,
        # 是否进行Spindle检测
        'spindle_detect': False,
        # 是否显示matplotlib绘图，一般不推荐
        'show_plots': False,
        # 是否绘制慢波增强对比图(ERP图)
        'plot_sw_stim_sham': True,
        # 是否绘制睡眠分期图
        'plot_sleep_fig': True
    }
    # 在线下载并分析
    # download_and_full_analyse(download_param, analyse_param)

    # 直接本地分析
    local_datas_full_analyse(r'E:\dataset\dev_test_data',
                             [
                                 # "chengyin01",
                                 # "chengyin02",
                                 # "kongte01",
                                 # "laonianren01",
                                 # "laonianren02",
                                 # "zhangzhe01",
                                 # "zhangzhe02",
                                 # "zhangzhe03"

                                 # "sunyu01",
                                 # "sunyu02",
                                 # "sunyu03",
                                 # "zhangqin04",
                                 # "zhangqin05",
                                 # "zhangqin03",
                                 # "18618188432_20231011_12_04_08_20231012_06_52_14",
                                 # "18631314801_20231129_16_54_01_20231130_08_02_48",
                                 # "15011018788_20230914_13_21_30_20230915_09_15_13",
                                 # "15011018788_20230914_13_21_30_20230915_09_15_13",
                                 # "18618188432_20231010_16_54_43_20231011_12_00_24",
                                "15256003642_1227-22_16_49_1228-09_11_19_-0.00_4"
                             ],

                             r'E:\dataset\dev_test_data', analyse_param=analyse_param)


