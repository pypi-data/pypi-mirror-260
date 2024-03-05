import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.io import loadmat
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import f1_score, accuracy_score

"""
当前脚本主要用于绘制自动分期与手工分期的对比
"""
def plot_prediction_sleepstaging(targets, predictions, class_label, time_unit=15, title="", save_path=None):
    """
    绘制手工分期与自动分期对比
    :param targets: 手工分期结果
    :param predictions: 自动分期结果
    :param class_label: 类别标签
    :param time_unit: 时间单位
    :param title: 图片标题
    :param save_path: 图片保存路径
    :return:
    """
    targets = np.array(targets).squeeze()
    predictions = np.array(predictions).squeeze()

    targets_min = np.min(targets)
    targets_max = np.max(targets)

    predictions_min = np.min(predictions)
    predictions_max = np.max(predictions)

    distance = max(predictions_max, targets_max) - min(predictions_min, targets_min) + 1

    num_class = len(class_label)

    assert distance == num_class, "The range of input hypnos don't match the class count"

    hypno_min = min(targets_min, predictions_min)
    hypno_max = max(targets_max, predictions_max)

    fig, ax = plt.subplots(2, 1, figsize=(12, 4))
    fig.subplots_adjust(hspace=0.5)

    print(classification_report(targets, predictions, target_names=class_label))
    f1 = f1_score(targets, predictions, average='weighted')
    accuracy = accuracy_score(targets, predictions)

    sns.despine()
    t = np.arange(targets.shape[0]) / (3600 / time_unit)
    ax[0].plot(t, targets, lw=1.5, color='k')
    ax[0].set_ylim([hypno_min - 0.02, hypno_max])
    ax[0].set_yticks(list(range(hypno_min, hypno_max + 1)))
    ax[0].set_yticklabels(class_label)
    ax[0].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    # ax[0].set_title('Alpha Corr = {:.2f}'.format(corr_alpha), loc='right')
    ax[0].grid(visible=True, axis='y', linewidth=0.3)

    ax[1].plot(t, predictions, lw=1.5, color='r')
    ax[1].set_ylim([hypno_min - 0.02, hypno_max])
    ax[1].set_yticks(range(hypno_min, hypno_max + 1))
    ax[1].set_yticklabels(class_label)
    ax[1].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax[1].set_title('Accuracy: {:.2f}%, F1 Score: {:.2f}%'.format(accuracy * 100, f1 * 100), y=1, loc='right')
    ax[1].text(0.95, 0.05, title, ha='right', va='bottom', transform=plt.gca().transAxes)
    ax[1].grid(visible=True, axis='y', linewidth=0.3)

    ax[1].spines['top'].set_visible(False)
    ax[1].spines['right'].set_visible(False)
    ax[1].spines['bottom'].set_visible(False)
    ax[1].spines['left'].set_visible(False)
    ax[0].spines['top'].set_visible(False)
    ax[0].spines['right'].set_visible(False)
    ax[0].spines['bottom'].set_visible(False)
    ax[0].spines['left'].set_visible(False)

    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_bland_altman(ground_truth, prediction, title_x="", title_y="", save_path=None):
    """
    基于手工分期结果和自动分期结果，计算各个睡眠指标，然后使用手工分期的睡眠指标作为金标准，绘制Bland-Altman图
    :param ground_truth: 金标准（手工分期结果的某个睡眠指标）
    :param prediction: 自动分期的对应睡眠指标
    :param title_x: x轴标题
    :param title_y: y轴标题
    :param save_path: 图片保存路径
    :return:
    """
    ground_truth = np.array(ground_truth).squeeze()
    prediction = np.array(prediction).squeeze()
    assert ground_truth.shape[0] == prediction.shape[0], "The length of ground truth doesn't match the prediction's."
    fig, ax = plt.subplots(1, 1, figsize=(5, 4))

    diff = prediction - ground_truth
    diff_min = np.min(diff)
    diff_max = np.max(diff)
    mean_tst = np.mean(diff)
    sd_tst = np.std(diff, axis=0)

    ax.scatter(ground_truth, diff, color='black', s=20)
    ax.axhline(mean_tst, color='red', linestyle='-')
    ax.axhline(mean_tst + 1.96 * sd_tst, color='red', linestyle='--')
    ax.axhline(mean_tst - 1.96 * sd_tst, color='red', linestyle='--')
    ax.axhline(0, color='black', linestyle='-')
    ax.set_xlabel(title_x)
    ax.set_ylabel(title_y)
    ax.set_ylim([diff_min * 1.2, diff_max * 1.2])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plotConfusionMatrix(target, prediction, class_count, labels, is_percentage, title_x="", title_y="", save_path=None):
    """
    绘制混淆矩阵
    :param target: 手工分期结果
    :param prediction: 自动分期结果
    :param class_count: 分类类别数
    :param labels: 分类类别标签
    :param is_percentage: 是否显示百分比
    :param title_x: x轴标题
    :param title_y: y轴标题
    :param save_path: 图片保存路径
    :return:
    """

    # class_count = 4  # 这个数值是具体的分类数，大家可以自行修改
    # labels = ['N3', 'N1/N2', 'REM', 'Wake']  # 每种类别的标签

    epoch_to_drop = np.union1d(np.where(prediction == 5)[0], np.where(target == 5)[0])
    prediction = np.delete(prediction, epoch_to_drop)
    target = np.delete(target, epoch_to_drop)

    cmatrix = confusion_matrix(target, prediction)
    plt.rcParams["font.family"] = ["sans-serif"]
    plt.rcParams["font.sans-serif"] = ['SimHei']
    plt.figure(figsize=(8, 6))
    # 显示数据

    # 在图中标注数量/概率信息
    thresh = cmatrix.max() / 2  # 数值颜色阈值，如果数值超过这个，就颜色加深。
    for x in range(class_count):
        row_sum = np.sum(cmatrix, axis=1)
        for y in range(class_count):
            # 注意这里的matrix[y, x]不是matrix[x, y]
            info = int(cmatrix[y, x])
            if is_percentage:
                percentage = str(int(0 if row_sum[y] == 0 else cmatrix[y][x] / row_sum[y] * 10000) / 100)
                percentage += "%"
                percentage = "{}({})".format(cmatrix[y][x], percentage)
                plt.text(x, y, percentage,
                         verticalalignment='center',
                         horizontalalignment='center',
                         color="white" if info > thresh else "black")
            else:
                plt.text(x, y, info,
                         verticalalignment='center',
                         horizontalalignment='center',
                         color="white" if info > thresh else "black")

    row_sum = np.sum(cmatrix, axis=1)
    cmatrix = cmatrix.astype(dtype=np.float)
    for x in range(class_count):
        for y in range(class_count):
            cmatrix[x][y] = cmatrix[x][y] / row_sum[x]
    plt.imshow(cmatrix, cmap=plt.cm.Reds)
    plt.yticks(range(class_count), labels, fontsize=12)
    plt.ylabel(title_y, labelpad=10, fontdict={'fontsize': 15})
    plt.xlabel(title_x, labelpad=10, fontdict={'fontsize': 15})
    plt.xticks(range(class_count), labels, fontsize=12)
    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    # targets = [0, 1, 2, 3, 4, 1, 1, 2, 3, 2, 1, 2, 3, 4]
    # predictions = [0, 1, 4, 2, 3, 1, 1, 2, 3, 2, 1, 4, 3, 4]
    # label = ['N3', "N12", "REM", "Wake", "Abnormal"]
    # plot_prediction_sleepstaging(targets, predictions, label)
    #
    # plot_bland_altman(targets, predictions, "sadasdas", "1111111111111")
    data_par_path = r"E:\dataset\x7_XSR"
    datas = [
        '35_unlabel_20231128_175938',
        '36_unlabel_20231201_182809',
        '37_unlabel_20231202_192343',
        '38_unlabel_20231203_182305',
        '39_unlabel_20231206_180746',
        '40_unlabel_20231207_174611',
        '41_unlabel_20231208_181218',
        '42_unlabel_20231209_180300',

        # '32_20231118_164926',
        # '33_20231122_182132',
        # '34_20231123_162036'
    ]
    for data in os.listdir(data_par_path):
        if data in datas:
            target = loadmat(os.path.join(os.path.join(data_par_path, data), "psg_trans_label.mat"))['psg_trans_label']
            prediction = loadmat(os.path.join(os.path.join(data_par_path, data), "prediction.mat"))['prediction']
            target[target <= 0] = 0


            target[target == 5] = 2
            target[target == 4] = 3

            # prediction[prediction == 5] = 2
            # prediction[prediction == 4] = 3

            plot_prediction_sleepstaging(target, prediction, ["0", "1", "2", "3"])
