import numpy as np
import lightgbm as lgb
import pandas as pd
from lmsleepdata.postprocess.label_smooth import pp_label_smooth
import os


def load_model(use_acc, use_time, context_mode):
    """
    加载模型：通过是否使用acc特征、time特征、上下文模式来选取合适的模型。但目前只有2种模型可选（wholenight和realtime，都没有acc和time特征）
    :param use_acc: 是否使用acc特征
    :param use_time: 是否使用time特征
    :param context_mode: 上下文模式
    :return:
    """
    model_name = "sleep_staging.txt"
    if use_acc:
        model_name = 'acc_' + model_name

    if use_time:
        model_name = 'time_' + model_name

    if context_mode == 2:
        model_name = "wholenight_" + model_name
    elif context_mode == 1:
        model_name = "realtime_" + model_name

    base_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(base_path)
    dir_path = os.path.join(dir_path, "../models")
    clf = lgb.Booster(model_file=os.path.join(dir_path, model_name))
    return clf

def sleep_staging_with_features(features, clf):
    """
    根据输入的模型和特征进行睡眠分期，class count等于3,4,5的时候分别对应新生儿分期、成人模糊分期、成人精确分期
    :param features: DataFrame形式的特征集
    :param clf: LightGBM模型
    :return:
    """
    feature_name = clf.feature_name()
    class_count = clf._Booster__num_class
    feature_for_predict = features[feature_name]
    raw_score = clf.predict(feature_for_predict)
    # for i in clf.feature_name():
    #     print("{}: {}".format(i, feature_for_predict.loc[2][i]))

    # for i in range(raw_score.shape[0]):
    #     print("epoch: {}, raw score: {:.5f}".format(i, max(raw_score[i])))

    predictions = np.argmax(raw_score, axis=1)

    if class_count == 5:
        # 5分类分期容易把REM和N2分成N1，因此对N1的结果进行调整
        # raw_n3 = np.where(predictions == 2)[0]
        # excluded_n3 = raw_n3[np.where(raw_score[:, 2][raw_n3] < 0.75)[0]]
        # predictions[excluded_n3] = 1
        #
        # raw_n1 = np.where(predictions == 0)[0]
        # excluded_n1 = raw_n1[np.where(raw_score[:, 0][raw_n1] < 0.8)[0]]
        # excluded_n1_to_wake = excluded_n1[np.where(raw_score[:, 4][excluded_n1] > raw_score[:, 3][excluded_n1])[0]]
        # excluded_n1_to_rem = excluded_n1[np.where(raw_score[:, 4][excluded_n1] < raw_score[:, 3][excluded_n1])[0]]
        # predictions[excluded_n1_to_wake] = 4
        # predictions[excluded_n1_to_rem] = 3

        classes_with_alphabet_order = np.array(['N1', 'N2', 'N3', 'REM', 'Wake'])
        predictions = classes_with_alphabet_order[predictions]
        df_hypno = pd.Series(predictions)
        df_hypno.replace({'N3': 0, 'N2': 1, 'N1': 2, 'REM': 3, 'Wake': 4}, inplace=True)
    elif class_count == 4:
        classes_with_alphabet_order = np.array(['N1/N2', 'N3', 'REM', 'Wake'])
        predictions = classes_with_alphabet_order[predictions]
        df_hypno = pd.Series(predictions)
        df_hypno.replace({'N3': 0, 'N1/N2': 1, 'REM': 2, 'Wake': 3}, inplace=True)
    elif class_count == 3:
        classes_with_alphabet_order = np.array(['Wake', 'AS', 'QS'])
        predictions = classes_with_alphabet_order[predictions]
        df_hypno = pd.Series(predictions)
        df_hypno.replace({'Wake': 1, 'AS': 2, 'QS': 3}, inplace=True)

    predictions = df_hypno.to_numpy()


    return predictions
