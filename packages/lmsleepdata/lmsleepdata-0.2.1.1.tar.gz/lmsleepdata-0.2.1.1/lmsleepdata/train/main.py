import os

import numpy as np
from scipy.io import savemat, loadmat

from lm_datahandler.train.dataload_and_train import train
from lm_datahandler.train.predict_and_plot import model_predict_simple, plot_comparison


# todo：指定训练模型时的class_label
class_label = {0: 'N3', 1: 'N1/N2', 2: 'REM', 3: 'Wake'}

def model_train():

    # todo：根据当前的任务，修改类别标签和类别权重
    class_weight = {'N3': 2, 'N1/N2': 1, 'REM': 1, 'Wake': 2}

    # 一般不需要改
    train_params = dict(
        boosting_type='gbdt',
        n_estimators=120,
        max_depth=4,
        num_leaves=15,
        colsample_bytree=0.5,
        importance_type='gain',
        n_jobs=4
    )

    # todo: 指定训练集和验证集的路径
    train_data_path = "dataset/realtime_tail_eeg_20240110.parquet"
    validate_data_path = None

    # todo：指定模型文件名
    model_name = "realtime_sleepstaging_tail_eeg_20240110.txt"
    train(train_data_path, validate_data_path, train_params, class_label, class_weight, model_name)


# 实时预测场景中，使用p8/p4（单位为epoch，不是分钟）等往期小窗口平均作为特征的预测效果较差，但仿照整夜分析的方案，使用P15则效果上升
# 使用P15时，P15(t=0) = C15(t=-7)，即相当于延迟版的整夜分析
# 因此，效果能够和整夜分析的效果类似，但是存在1~2分钟的延迟

def batch_prediction():
    # 自动寻找最新的模型
    with open('model_name.txt', 'r') as f:
        model_path_1 = list(f.readlines())[-1].strip()

    # todo：指定好要预测的数据，包括父路径和数据目录名
    data_par_path = r"E:\dataset\x7_tail\1_37"
    datas = [
        # "chengyin01",
        # "chengyin02",
        # "kongte01",
        # "laonianren01",
        # "laonianren02",
        # "zhangzhe01",
        # "zhangzhe02",
        "15112163029_20231120_20_04_50_20231121_07_56_13",
        "13547951033_20230913_22_47_04_20230914_07_19_54"
    ]


    for data in os.listdir(data_par_path):
        if data in datas:
            temp_path = os.path.join(data_par_path, data)
            print("------------" + data + " start ------------------")
            temp_predictions = model_predict_simple(temp_path, model_path=model_path_1, class_label=class_label)
            savemat(os.path.join(os.path.join(data_par_path, data), "prediction.mat"), {"prediction": temp_predictions})
            # print(np.array(temp_predictions))
            # todo: 指定金标准分期的文件名，用于绘制对比图
            if os.path.exists(os.path.join(temp_path, "hypno.mat")):
                hypno = loadmat(os.path.join(temp_path, "hypno.mat"))["hypno"].squeeze()
                plot_comparison(temp_predictions, hypno, class_label)


def main():
    # model_train()
    batch_prediction()

if __name__ == "__main__":
    main()
