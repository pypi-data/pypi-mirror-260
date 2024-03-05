import numpy as np
import lightgbm as lgb
import pandas as pd
from lmsleepdata.postprocess.label_smooth import pp_label_smooth
import os

def wear_detect_with_features(features, model_path):
    """
    佩戴检测
    :param features: DataFrame形式的特征
    :param model_path: 外部输入的佩戴检测模型路径，为None的话使用内置模型
    :return:
    """
    if model_path is not None:
        clf = lgb.Booster(model_file=model_path)
    else:
        model_name = "wear_detection_1s.txt"
        base_path = os.path.abspath(__file__)
        dir_path = os.path.dirname(base_path)
        dir_path = os.path.join(dir_path, "../models")
        clf = lgb.Booster(model_file=os.path.join(dir_path, model_name))

    # create and select features

    feature_name = clf.feature_name()
    feature_for_predict = features[feature_name]

    predictions = clf.predict(feature_for_predict)


    predictions = np.asarray(predictions, dtype=np.float)

    return predictions
