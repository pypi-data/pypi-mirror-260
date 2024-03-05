import lightgbm as lgb
import numpy as np
import pandas as pd

from lm_datahandler.plots.metrics_plot import plot_prediction_sleepstaging
from lm_datahandler.train.mat_to_npz_new import new_datahandler_load_mat_without_hypno
from lm_datahandler.train.post_process import pp_label_smooth
from lm_datahandler.train.plot_prediction import plotConfusionMatrix


def model_predict_simple(predict_data_path, model_path, class_label):
    """
    使用测试集数据和模型进行简单预测（不包含绘图等）
    :param predict_data_path: 待预测数据路径
    :param model_path: 待预测模型路径
    :param class_label: 标签名
    :return: 预测结果
    """

    # 使用和生成训练集同样的方式生成当前测试数据的特征
    features, data_handler = new_datahandler_load_mat_without_hypno(predict_data_path)


    # 加载模型，并检查提取的特征和模型所需的特征是一致的
    clf = lgb.Booster(model_file=model_path)
    feature_count = len(clf.feature_name())
    assert feature_count == features.shape[1], "The feature doesn't match the model."
    target_feature_name = clf.feature_name()
    target_feature = features[target_feature_name]
    assert feature_count == target_feature.shape[1], "The feature doesn't match the model."

    raw_score = clf.predict(target_feature)
    predictions = np.argmax(raw_score, axis=1)

    # LightGBM的输出结果顺序是按照字典序排序的，所以这里需要变成指定的class_label的顺序
    classes_with_alphabet_order = np.array(sorted(class_label.values()))
    predictions = classes_with_alphabet_order[predictions]
    flipped_dict = {v: k for k, v in class_label.items()}
    df_hypno = pd.Series(predictions)
    df_hypno.replace(flipped_dict, inplace=True)
    predictions = df_hypno.to_numpy()

    # todo: 是否进行结果平滑，不用就注释掉
    predictions = pp_label_smooth(np.copy(predictions), window=2)

    return predictions


def plot_comparison(predictions, hypno, class_label):
    """
    绘制预测结果与金标准对比图
    :param predictions: 预测结果
    :param hypno: 金标准
    :param class_label: 分类类别标签
    :return:
    """

    # 将在class_label最大值和最小值范围之外的标签认为是异常标签
    # 并将异常标签从预测结果和金标准中都剔除，换言之，对比结果是不包含异常标签的
    min_class = min(class_label.keys())
    max_class = max(class_label.keys())
    abnormal_indices = np.union1d(np.where(hypno < min_class)[0], np.where(hypno > max_class)[0])
    predictions = np.delete(predictions, abnormal_indices)
    hypno = np.delete(hypno, abnormal_indices)

    # df_hypno = pd.Series(predictions)
    # df_hypno.replace(class_label, inplace=True)

    plot_prediction_sleepstaging(hypno, predictions, class_label.values())

    plotConfusionMatrix(predictions, hypno, len(class_label), class_label.values(), True, save_path=None)




