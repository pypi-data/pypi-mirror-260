import datetime
from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from matplotlib import gridspec
from scipy.io import loadmat
from scipy.stats import pearsonr
import matplotlib.dates as mdates
from matplotlib.colors import Normalize
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
import os
from lspopt import spectrogram_lspopt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.manifold import TSNE


"""
聚类绘图：不属于工具包的核心功能，用于额外对数据进行聚类分析
"""
def sample_points_cluster(X, decomposition, n_components, num_clusters, cluster_method='KMeans'):
    """
    样本点聚类
    :param X: 样本点
    :param decomposition: 降维方法：PCA/LDA/TSNE/None
    :param n_components: 降维后维数，降维方法不为None时，一般降到2维，方便绘图
    :param num_clusters: 聚类目标类别数
    :param cluster_method: 聚类方法：KMeans/AgglomerativeClustering
    :return:
    """
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    X = (X - mean) / std

    # 创建PCA对象并指定降维后的维度
    if decomposition == 'PCA':
        pca = PCA(n_components=n_components)
        X_reduced = pca.fit_transform(X)
    elif decomposition == 'LDA':
        lda = LinearDiscriminantAnalysis(n_components=n_components)
        X_reduced = lda.fit_transform(X)
    elif decomposition == 'TSNE':
        tsne = TSNE(n_components=n_components)
        X_reduced = tsne.fit_transform(X)
    else:
        X_reduced = X

    # 创建KMeans对象并指定聚类数量
    if cluster_method == 'KMeans':
        clustering = KMeans(n_clusters=num_clusters)
    elif cluster_method == 'AgglomerativeClustering':
        clustering = AgglomerativeClustering(n_clusters=num_clusters)

    # 对降维后的数据进行聚类
    clustering.fit(X_reduced)

    # 获取聚类结果
    labels = clustering.labels_

    if decomposition is not None and n_components == 2:
        for i in range(num_clusters):
            x_i = np.squeeze(X_reduced[:, 0])[np.where(labels == i)]
            y_i = np.squeeze(X_reduced[:, 1])[np.where(labels == i)]
            # plt.scatter(x_i, y_i, marker='o', color='blue', label='Insomnia & Cluster 1')
            plt.scatter(x_i, y_i, label='Cluster {}'.format(i))

        title = '{}({} Clusters)'.format(cluster_method, num_clusters)
        if decomposition is not None:
            title = "{} with {}({} Dimension)".format(title, decomposition, n_components)
        plt.title(title)
        plt.xlabel('Decomposition 1')
        plt.ylabel('Decomposition 2')
        plt.legend()
        plt.show()

    if decomposition is not None:
        feature_name = X.columns.to_numpy()
        for i in range(n_components):
            pca_i = np.squeeze(X_reduced[:, i])

            for j in range(feature_name.__len__()):
                feature_j = X.values[:, j]
                corr, p = pearsonr(pca_i, feature_j)
                print("{} with PCA{}: corr = {}, p = {}".format(feature_name[j], i, corr, p))

    return labels


def plot_spectrogram(fig, ax, eeg, start_time, sf=500, win=15, freq_band=(0.5, 50), cmap="RdBu_r", trim_percentage=5,
                     vmin=None, vmax=None):
    """
    绘制时频图
    """
    cmap = "Spectral_r"
    assert isinstance(eeg, np.ndarray), "Data must be a 1D NumPy array."
    assert isinstance(sf, (int, float)), "sf must be int or float."
    assert eeg.ndim == 1, "Data must be a 1D (single-channel) NumPy array."
    assert isinstance(win, (int, float)), "win_sec must be int or float."
    assert isinstance(freq_band, tuple) and freq_band.__len__() == 2, "freq_band must be tuple with 2 numbers."
    assert isinstance(freq_band[0], (int, float)), "freq[0] must be int or float."
    assert isinstance(freq_band[1], (int, float)), "freq[1] must be int or float."
    assert freq_band[0] < freq_band[1], "fmin must be strictly inferior to fmax."
    assert freq_band[1] < sf / 2, "fmax must be less than Nyquist (sf / 2)."
    # assert isinstance(vmin, (int, float, type(None))), "vmin must be int, float, or None."
    # assert isinstance(vmax, (int, float, type(None))), "vmax must be int, float, or None."

    nperseg = int(win * sf)
    assert eeg.size > 2 * nperseg, "Data length must be at least 2 * win_sec."
    f, t, Sxx = spectrogram_lspopt(eeg, sf, nperseg=nperseg, noverlap=0)
    Sxx = 10 * np.log10(Sxx)  # Convert uV^2 / Hz --> dB / Hz
    # Select only relevant frequencies (up to 30 Hz)
    good_freqs = np.logical_and(f >= freq_band[0], f <= freq_band[1])
    Sxx = Sxx[good_freqs, :]
    f = f[good_freqs]
    # savemat('E:/dataset/dev_test_data/'+start_time.strftime("%Y%m%d_%H%M%S")+'.mat', {'Sxx':Sxx, 'freq': f})
    Sxx[Sxx < -15] = -15
    t /= 3600  # Convert t to hours

    timestamp = [start_time + timedelta(hours=hours) for hours in t]
    timestamp_num = mdates.date2num(timestamp)
    vmin_per, vmax_per = np.percentile(Sxx, [0 + trim_percentage, 100 - trim_percentage])
    if vmin is None:
        vmin = vmin_per
    else:
        vmin = max(vmin_per, vmin)
    if vmax is None:
        vmax = vmax_per
    else:
        vmax = min(vmax_per, vmax)

    norm = Normalize(vmin=vmin, vmax=vmax)
    im = ax.pcolormesh(timestamp_num, f, Sxx, norm=norm, cmap=cmap, antialiased=True, shading="auto")
    # ax.set_xlim(0, timestamp_num.max())
    ax.xaxis_date()
    ax.set_ylim([0, 50])
    ax.set_yticks([5, 10, 15, 20, 25, 30, 35, 40, 45, 50])

    ax.tick_params(axis='y', labelsize=14)
    ax.tick_params(axis='x', labelsize=14)
    ax.set_ylabel("Frequency [Hz]", fontdict={"fontsize": 18})
    ax.set_xlabel("Time [hrs]", fontdict={"fontsize": 18})
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    # extra_ticks = [timestamp_num[0], timestamp_num[-1]]  # 最小值和最大值
    # ax.set_xticks(list(ax.get_xticks()) + extra_ticks)

    return fig, ax, im

def plot_cluster_result(fig, ax, hypno, start_time, win=15):
    """
    绘制聚类结果
    """
    assert len(hypno.shape) == 1, "Hypno should be a 1-D array"

    t = np.arange(hypno.size) * win / 3600
    timestamp = [start_time + timedelta(hours=hours) for hours in t]
    timestamp_num = mdates.date2num(timestamp)

    hypno_min = min(hypno)
    hypno_max = max(hypno)
    ax.plot(timestamp_num, hypno, lw=2, color='k')
    for label in range(hypno_min, hypno_max + 1):
        label_index = np.ma.masked_not_equal(hypno, label)
        if len(label_index) == 0:
            continue
        ax.plot(timestamp_num, label_index, lw=2)

    ax.set_ylim([hypno_min-0.1, hypno_max+0.8])
    ax.set_yticks(list(range(hypno_min, hypno_max + 1)))
    tick_labels = list(range(hypno_min, hypno_max + 1))
    tick_labels = ["label " + str(i) for i in tick_labels]
    ax.set_yticklabels(tick_labels)
    ax.tick_params(axis='y', labelsize=14)
    ax.tick_params(axis='x', labelsize=14)
    ax.set_ylabel("Cluster Result", fontdict={"fontsize": 18})
    ax.set_xlabel("Time [hrs]", fontdict={"fontsize": 18})

    # extra_ticks = [timestamp_num[0], timestamp_num[-1]]  # 最小值和最大值
    # ax.set_xticks(list(ax.get_xticks()) + extra_ticks)

    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set_xlim([timestamp_num[0], timestamp_num[-1]])
    return fig, ax

def plot_cluster_label_with_spectral(eeg, hypno, start_time):
    """
    将聚类结果作为分期结果，然后结合时频图一起绘制
    """
    # start_time = datetime.datetime.timestamp(start_time)
    fig_height = 5 + 4
    height_ratio = (np.ones(2) * 4).tolist()
    plot_spectral = True
    plot_cluster = True
    if plot_spectral:
        height_ratio[0] = 5.0
    # fig, ax = plt.subplots(subplot_count, 1, figsize=(16, fig_height), height_ratio=height_ratio)
    fig = plt.figure(figsize=(20, fig_height))
    gs = gridspec.GridSpec(2, 1, height_ratios=height_ratio)
    # fig.subplots_adjust(hspace=0.5)
    # if subplot_count == 1:
    #     ax = [ax]

    i = 0
    if plot_spectral:
        ax_1 = fig.add_subplot(gs[i, 0])
        plot_spectrogram(fig, ax_1, eeg, start_time, 500)
        i += 1

    if plot_cluster:
        ax_2 = fig.add_subplot(gs[i, 0])
        plot_cluster_result(fig, ax_2, hypno, start_time)

    plt.tight_layout()
    plt.show()


def generate_dataset_with_name(data_path):
    df = pd.read_parquet(data_path)
    df = df.dropna(axis=0)
    cols_all = df.columns

    cols_instance_eeg = cols_all[cols_all.str.startswith('eeg') &
                                 ~(cols_all.str.endswith('_norm'))].tolist()
    cols_n3 = cols_all[cols_all.str.startswith('n3')].tolist()
    cols_n12 = cols_all[cols_all.str.startswith('n12')].tolist()
    cols_rem = cols_all[cols_all.str.startswith('rem')].tolist()
    cols_demo = ['tst', 'sol', 'waso', 'se', 'sw_total', 'sw_n3', 'sp_total', 'sp_n12', 'age', 'sex']

    # feature_columns = [] + cols_n12 + cols_rem + cols_n3 + cols_demo
    feature_columns = [] + cols_instance_eeg

    X = df[feature_columns]
    # y = df['label']
    # name = df['data_name']
    # source = df['data_source']
    # y.replace({0: '0', 1: '1'}, inplace=True)
    # return X, y, name, source
    return X


if __name__ == '__main__':


    data_path = r"E:\dataset\x7_ZWR\18631314801_20231129_16_54_01_20231130_08_02_48"
    sample_points = generate_dataset_with_name(os.path.join(data_path, "features.parquet"))

    # 降维和聚类
    label = sample_points_cluster(sample_points, decomposition="TSNE", n_components=2, num_clusters=5,
                                  cluster_method='KMeans')

    eeg_and_acc = loadmat(os.path.join(data_path, "eeg_and_acc.mat"))
    data_name = os.path.basename(data_path)
    start_time = datetime.datetime.strptime(data_name[12:12+17], "%Y%m%d_%H_%M_%S")

    plot_cluster_label_with_spectral(eeg_and_acc['eeg'].squeeze(), label, start_time)

    sample_people_1 = sample_points[label == 0]
    sample_people_2 = sample_points[label == 1]
    sample_people_3 = sample_points[label == 2]
    # sample_people_4 = sample_points[label == 3]
    sample_people_cluster = [sample_people_1, sample_people_2, sample_people_3]
    # feature_name = ["TST", "SL", "WASO", "AR", "SE", "N3", "N12", "REM", "Total SW", "N3 SW", "Total SP", "N12_SP"]
    feature_name = sample_points.columns.tolist()
    for i in range(3):
        print("sample points mean and std in cluster {}".format(i + 1))
        for j in range(feature_name.__len__()):
            print("{}: {:.2f} ± {:.2f}".format(feature_name[j], np.mean(sample_people_cluster[i].values[:, j]),
                                               np.std(sample_people_cluster[i].values[:, j])))

    print("======================================================================")

    # print("Sample point are clustered as:")
    # str_people = str(sample_points_name[0]) + "[" + str(label[0])
    # current_name = sample_points_name[0]
    # for i in range(1, len(sample_points)):
    #     if sample_points_name[i] == current_name:
    #         str_people = str_people + ", " + str(label[i])
    #     else:
    #         str_people = str_people + "]"
    #         print(str_people)
    #         str_people = str(sample_points_name[i]) + "[" + str(label[i])
    #         current_name = sample_points_name[i]
    # str_people = str_people + "," + str(label[-1]) + "]"
    # print(str_people)
    # # print("{} - {}: {}".format(sample_points_name[i], sample_points_dates[i], label[i]))
    #
    # print("======================================================================")

    # print(" ")
    # print("sample_points: {}\ncenter point: {}".format(label, centroid))

    # corr_analysis(sample_people[1], "test1", sample_people[2], "test2")
    # 特征单独提取
    # sl = np.asarray(sample_people[:, 0], dtype=np.float32)
    #
    # n3_time = np.asarray(sample_people[:, 1], dtype=np.float32)
    # n12_time = np.asarray(sample_people[:, 2], dtype=np.float32)
    # rem_time = np.asarray(sample_people[:, 3], dtype=np.float32)
    #
    # total_time = n3_time + n12_time + rem_time
    #
    # sw_count = np.asarray(sample_people[:, 5], dtype=np.float32)
    # sw_n3_count = np.asarray(sample_people[:, 6], dtype=np.float32)
    # sp_count = np.asarray(sample_people[:, 7], dtype=np.float32)
    # sp_n12_count = np.asarray(sample_people[:, 8], dtype=np.float32)
    #
    # psqi = np.asarray(sample_people[:, 9], dtype=np.float32)
    # psqi_sleep_equality = np.asarray(sample_people[:, 10], dtype=np.float32)
    # psqi_sleep_time = np.asarray(sample_people[:, 11], dtype=np.float32)
    # psqi_sleep_efficiency = np.asarray(sample_people[:, 12], dtype=np.float32)
    #
    # scl_90 = np.asarray(sample_people[:, 13], dtype=np.float32)
    # scl_ocd = np.asarray(sample_people[:, 14], dtype=np.float32)
    # scl_de = np.asarray(sample_people[:, 15], dtype=np.float32)
    # scl_an = np.asarray(sample_people[:, 16], dtype=np.float32)
    #
    # desr = np.asarray(sample_people[:, 17], dtype=np.float32)
    # desr_1 = np.asarray(sample_people[:, 18], dtype=np.float32)
    # desr_2 = np.asarray(sample_people[:, 19], dtype=np.float32)
    # desr_3 = np.asarray(sample_people[:, 20], dtype=np.float32)
    # desr_4 = np.asarray(sample_people[:, 21], dtype=np.float32)
    # desr_5 = np.asarray(sample_people[:, 22], dtype=np.float32)
    # desr_6 = np.asarray(sample_people[:, 23], dtype=np.float32)

    # 选择特征做相关分析
    # corr_analysis(n12_time/n3_time, "n12_time/n3_time", scl_de, "SCL Depression")

# correlation, p_value = pearsonr(total_time, -1*psqi)
# print("n3_time vs psqi: corr = {}, p = {}".format(correlation, p_value))
#
# correlation, p_value = pearsonr(total_time, -1*psqi_sleep_equality)
# print("n3_time vs psqi_sleep_equality: corr = {}, p = {}".format(correlation, p_value))
#
# correlation, p_value = pearsonr(total_time, -1*psqi_sleep_time)
# print("n3_time vs psqi_sleep_time: corr = {}, p = {}".format(correlation, p_value))
#
# correlation, p_value = pearsonr(total_time, -1*psqi_sleep_efficiency)
# print("n3_time vs psqi_sleep_efficiency: corr = {}, p = {}".format(correlation, p_value))
#
# correlation, p_value = pearsonr(total_time, -1*scl_90)
# print("n3_time vs scl_90: corr = {}, p = {}".format(correlation, p_value))
#
# correlation, p_value = pearsonr(total_time, -1*scl_ocd)
# print("n3_time vs scl_ocd: corr = {}, p = {}".format(correlation, p_value))
#
# correlation, p_value = pearsonr(total_time, -1*scl_de)
# print("n3_time vs scl_de: corr = {}, p = {}".format(correlation, p_value))
#
# correlation, p_value = pearsonr(total_time, -1*scl_an)
# print("n3_time vs scl_an: corr = {}, p = {}".format(correlation, p_value))
#
#
#
# correlation, p_value = pearsonr(total_time, -1*desr_1)
# print("total_time vs desr_1: corr = {}, p = {}".format(correlation, p_value))
#
# correlation, p_value = pearsonr(total_time, -1*desr_2)
# print("total_time vs desr_2: corr = {}, p = {}".format(correlation, p_value))
#
# correlation, p_value = pearsonr(total_time, -1*desr_3)
# print("total_time vs desr_3: corr = {}, p = {}".format(correlation, p_value))
#
# correlation, p_value = pearsonr(total_time, -1*desr_4)
# print("total_time vs desr_4: corr = {}, p = {}".format(correlation, p_value))
#
# correlation, p_value = pearsonr(total_time, -1*desr_5)
# print("total_time vs desr_5: corr = {}, p = {}".format(correlation, p_value))
#
# correlation, p_value = pearsonr(total_time, -1*desr_6)
# print("total_time vs desr_6: corr = {}, p = {}".format(correlation, p_value))
#
#
# # plt.scatter(n3_time, psqi)
# # plt.xlabel('n3_time')
# # plt.ylabel('psqi')
# # plt.title('atterSc Plot')
#
# X = total_time
# X = sm.add_constant(X)
#
# Y = -1*scl_ocd + 30
# # 创建一个OLS模型
# model = sm.OLS(Y, X)
#
# # 拟合模型
# results = model.fit()
#
# # 打印回归结果
# print(results.summary())
#
# plt.scatter(total_time, -1*psqi)
#
# # plt.xlim([0.2, 1.5])
# # plt.ylim([0, 150])
# plt.xlabel('total_time')
# plt.ylabel('-1 * psqi')
# plt.title('corr = 0.40581\np = 0.06796', loc='right')
#
# plt.show()
#
# print(spearmanr(total_time, -1*scl_90))
# print(kendalltau(total_time, -1*scl_90))
