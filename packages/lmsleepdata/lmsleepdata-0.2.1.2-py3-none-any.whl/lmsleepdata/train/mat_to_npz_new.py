import os
import pandas as pd
import numpy as np
from lmsleepdata.datahandler import DataHandler
from scipy.io import loadmat
from lmsleepdata.train.self_define_feature_extract import LMFeature


"""
约定转换好的mat格式原始数据叫做：eeg_and_acc.mat，mat格式的标签文件叫做：hypno.mat
命名不同或者里面格式不同，可自行替换
"""
def new_datahandler_load_mat(mat_path):


    # todo: 指定标签数据的名字和格式
    hypno = loadmat(os.path.join(mat_path, "hypno.mat"))["hypno"]
    hypno = np.array(hypno).squeeze()

    features, data_handler = new_datahandler_load_mat_without_hypno(mat_path)
    epochs = len(features)
    hypno = hypno[:epochs]

    epoch = min(hypno.shape[0], features.shape[0])
    if hypno.shape[0] > epoch:
        hypno = hypno[0: epoch]
    if features.shape[0] > epoch:
        features = features.drop(features.index[epoch - features.shape[0]:])
    features['stage'] = hypno

    # todo: 剔除标签异常的epoch，只保留需要的类别，如正常睡眠分期范围从0~3，4为异常类别
    features = features[features["stage"] <= 3]
    features = features.reset_index(drop=True)
    return features, data_handler


def new_datahandler_load_mat_without_hypno(mat_path):
    data_handler = DataHandler()

    # todo：指定数据文件的名字
    eeg_and_acc = loadmat(os.path.join(mat_path, "eeg_and_acc.mat"))
    eeg = eeg_and_acc["eeg"]
    eeg = np.array(eeg).squeeze()

    epochs = eeg.shape[0] // (7500)
    eeg = eeg[0: epochs * 500 * 15]

    acc = eeg_and_acc["acc"]
    acc = np.array(acc).squeeze()
    acc = acc[:, 0:epochs * 50 * 15]



    data_handler.eeg = eeg
    data_handler.raw_eeg = eeg
    data_handler.acc = acc
    data_handler.raw_acc = acc
    data_handler.features['meta'] = {'male': 1, 'age': 30, 'data_type': 0, 'h/w': 0}
    eeg_sec = eeg.shape[0] // 500
    data_handler.seconds = eeg_sec

    data_handler.preprocess(filter_param={'highpass': 0.5, 'lowpass': None, 'bandstop': [[49, 51]]}, tailor_type='no')
    input_eeg = data_handler.eeg
    input_eeg = input_eeg[0:epochs * data_handler.sf_eeg * data_handler.epoch_len].reshape(-1,
                                                                                           data_handler.sf_eeg * data_handler.epoch_len)

    if data_handler.acc is not None:
        acc = data_handler.acc[:, 0:epochs * data_handler.sf_acc * data_handler.epoch_len]
        # acc = data['acc']
        accx = acc[0, :].reshape(-1, 1, 750)
        accy = acc[1, :].reshape(-1, 1, 750)
        accz = acc[2, :].reshape(-1, 1, 750)
        input_acc = np.concatenate([accx, accy, accz], axis=1)

    # todo: 这里根据自己的需求配置参数
    # 一般eeg是必备的，不要acc特征的话，把raw_acc置为None
    # context_mode与分期模式有关，如果是实时分期，则设置为1，如果是离线分期，则设置为2
    features = LMFeature(data_handler.features['meta'], raw_eeg=input_eeg, raw_acc=None,
                         sf_eeg=data_handler.sf_eeg, sf_acc=data_handler.sf_acc,
                         context_mode=1).get_features()

    return features, data_handler


def mat_data_to_npz(file_list):
    out_dir = 'E:/githome/lmsleepdata/lmsleepdata/train/dataset/'
    df = []
    data_file_list = open(file_list, 'r').readlines()
    data_list = [file[:-1] for file in data_file_list]

    for sub in data_list:
        data_path = sub
        features, _ = new_datahandler_load_mat(data_path)
        df.append(features)
        print("------------" + sub + " finished------------------")

    df = pd.concat(df)

    # df['dataset'] = "tail"

    # Convert to category
    # df['dataset'] = df['dataset'].astype('category')
    df['stage'] = df['stage'].astype('category')

    df = df.reset_index(drop=True)
    # %stage
    print(df['stage'].value_counts(normalize=True, sort=True))
    # Median value of the EEG IQR per stage
    print(df.groupby('stage')['eeg_iqr'].median())
    # Remove nights with a 9 in sleep stages
    # df.drop(index=df[df['stage'] == 9].index.get_level_values(0), level=0, inplace=True)

    # Number of unique nights in dataset
    print(df.index.get_level_values(0).nunique())
    # Export
    df.to_parquet(out_dir + 'realtime_tail_eeg_20240110.parquet')


def create_filelist():
    # todo: 修改数据集目录，以及数据列表文件名
    # 数据集目录
    list_dir = r'E:\dataset\x7_tail'
    # 数据列表文件
    list = r'./train_list_tail.txt'

    # 检查数据集目录里的所有数据，确保每套数据中都有eeg_and_acc.mat和hypno.mat两个文件
    f = open(list, 'a+')
    for data_name in os.listdir(list_dir):
        if os.path.isdir(os.path.join(list_dir, data_name)):
            file_all = os.listdir(os.path.join(list_dir, data_name))
            if 'eeg_and_acc.mat' in file_all and 'hypno.mat' in file_all:
                f.write(list_dir + "\\" + data_name + "\n")


if __name__ == '__main__':
    # create_filelist()
    mat_data_to_npz("./train_list_tail.txt")
