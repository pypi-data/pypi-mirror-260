import numpy as np
from lspopt import spectrogram_lspopt
from matplotlib import gridspec
from datetime import datetime, timedelta
from lm_datahandler.preprocess.filter import eeg_filter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import Normalize


def plot_spectrogram_with_label_points(ax, eeg, start_time, sf=500, win=15, freq_band=(0.5, 50),
                                       cmap="Spectral_r", trim_percentage=5, vmin=None, vmax=None):
    """
    时频图绘制，与sleep_staging_plot中略有差异，增加了标题以及返回值t
    :param ax: 子图
    :param eeg: 脑电信号
    :param start_time: 开始时间
    :param sf: 采样率
    :param win: 窗口大小
    :param freq_band: 待绘制频率范围
    :param cmap: 色图
    :param trim_percentage:
    :param vmin:
    :param vmax:
    :return:
    """
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
    #
    # if points is not None:
    #     points = points / 500.0 / 15 + mdates.date2num(start_time)
    #     ax.scatter(points, np.ones(len(points)) * 500, c="black")

    # extra_ticks = [timestamp_num[0], timestamp_num[-1]]  # 最小值和最大值
    # ax.set_xticks(list(ax.get_xticks()) + extra_ticks)

    return t

def plot_points_distribution(ax, t, start_time, stim_points=None, sham_points=None):
    """
    绘制Stim和Sham点在时间上的分布
    :param ax: 子图
    :param t: 时间范围
    :param start_time: 起始时间
    :param stim_points: Stim点坐标
    :param sham_points: Sham点坐标
    :return:
    """
    if stim_points is None:
        return
    stim_points = stim_points / 500.0 / 3600
    sham_points = sham_points / 500.0 / 3600

    stim_points_timestamp = [start_time + timedelta(hours=hours) for hours in stim_points]
    stim_points_timestamp_num = mdates.date2num(stim_points_timestamp)

    sham_points_timestamp = [start_time + timedelta(hours=hours) for hours in sham_points]
    sham_points_timestamp_num = mdates.date2num(sham_points_timestamp)

    timestamp = [start_time + timedelta(hours=hours) for hours in t]
    timestamp_num = mdates.date2num(timestamp)

    ax.scatter(stim_points_timestamp_num, np.ones(len(stim_points)) * 15, c="red")
    ax.scatter(sham_points_timestamp_num, np.ones(len(stim_points)) * 5, c="gray")

    ax.set_ylim([0, 20])
    ax.set_yticks([5, 15])
    ax.set_yticklabels(["Sham", "Stim"])

    ax.tick_params(axis='y', labelsize=14)
    ax.tick_params(axis='x', labelsize=14)
    # ax.set_ylabel("Stim", fontdict={"fontsize": 18})
    ax.set_xlabel("Time [hrs]", fontdict={"fontsize": 18})

    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set_xlim(timestamp_num[0], timestamp_num[-1])
    return ax

def plot_stim_vs_sham(ax, eeg, sf_eeg, stim_indicator, sham_indicator):
    """
    绘制Stim和Sham的慢波对比图
    :param ax: 子图
    :param eeg: 脑电信号
    :param sf_eeg: 采样率
    :param stim_indicator: Stim点坐标
    :param sham_indicator: Sham点坐标
    :return:
    """
    # data preprocess
    eeg = (eeg - 32767) / 65536 * 2.5 * 1000 * 1000 / 100

    eeg_filtered = eeg_filter(eeg, sf_eeg, 0.5, 3, 4, 3, [[49, 51]], 3)

    # plot EEG signal and stimulus timing
    # plot ERP of slow wave
    seg_downlim = 1  # ERP downlimitation
    seg_uplim = 4  # ERP uplimitation
    # EEG_phase = {'stim': np.zeros((1, int((seg_downlim + seg_uplim) * 500))),
    #              'sham': np.zeros((1, int((seg_downlim + seg_uplim) * 500)))}

    EEGT = {'stim': [], 'sham': []}
    EEGT['stim'] = np.array(
        [eeg_filtered[i - int(sf_eeg * seg_downlim):i + int(sf_eeg * seg_uplim)] for i in
         stim_indicator])
    EEGT['sham'] = np.array(
        [eeg_filtered[i - int(sf_eeg * seg_downlim):i + int(sf_eeg * seg_uplim)] for i in
         sham_indicator])

    stim_sem = np.std(EEGT['stim'], axis=0) / np.sqrt(len(EEGT['stim']) / 2)
    sham_sem = np.std(EEGT['sham'], axis=0) / np.sqrt(len(EEGT['sham']) / 2)

    t = np.arange(-500, 2000) / sf_eeg
    eeg_stim_mean = np.mean(EEGT['stim'], axis=0)
    eeg_sham_mean = np.mean(EEGT['sham'], axis=0)

    # fig2, ax2 = plt.subplots(1, 1, figsize=figuresize)
    # ax2.errorbar(t, eeg_stim_mean, yerr=stim_sem, label='STIM', alpha=0.1, color=ax1[0].lines[2].get_color())
    ax.errorbar(t, eeg_stim_mean, yerr=stim_sem, label='STIM', alpha=0.1, color='r')
    # ax2.errorbar(t, eeg_sham_mean, yerr=sham_sem, label='SHAM', alpha=0.1, color=ax1[0].lines[3].get_color())
    ax.errorbar(t, eeg_sham_mean, yerr=sham_sem, label='SHAM', alpha=0.1, color='k')

    onset_idx = 500
    offset_idx = int(onset_idx + 1.075 * sf_eeg)
    ax.scatter(t[[onset_idx, offset_idx]], eeg_stim_mean[[onset_idx, offset_idx]], c='r',
               label='STIM Timings')
    ax.scatter(t[[onset_idx, offset_idx]], eeg_sham_mean[[onset_idx, offset_idx]], c='g',
               label='SHAM Timings')

    ax.set_xlim([min(t), max(t)])

    ax.set_xlabel('Time (s)', fontsize=25)
    ax.set_ylabel('Voltage (uV)', fontsize=25)
    ax.tick_params(labelsize=25)
    ax.legend(fontsize=20, loc='upper right')



def plot_stim_sham_sw(device_type, eeg, start_time, indexs, sf_eeg, savefig):
    """
    绘制慢波增强图，子图共3幅：
    1. 时频图
    2. 刺激点时机图：与时频图结合可以验证刺激点所在的睡眠阶段
    3. 慢波对比图：奇偶校验中，Stim和Sham的慢波对比
    :param device_type: 设备类型：X7的刺激点记录的是包ID，X8记录的是点ID
    :param eeg: 脑电信号
    :param start_time: 开始时间
    :param indexs: 刺激点坐标（Stim和Sham轮流记录）
    :param sf_eeg: 采样率
    :param savefig: 保存路径
    :return:
    """
    indexs = np.asarray(indexs)
    assert indexs.shape[0] >= 10, "The count of stim/sham points is less than expected, at least 10 points are needed."

    if indexs.shape[0] % 2 == 1:
        indexs = indexs[:-1]
    stim_idx_T = indexs.reshape([-1, 2])
    stim_idx = np.squeeze(stim_idx_T[:, 0])
    sham_idx = np.squeeze(stim_idx_T[:, 1])

    stim_idx_total = []
    sham_idx_total = []

    stim_idx_total = np.concatenate((stim_idx_total, stim_idx))
    sham_idx_total = np.concatenate((sham_idx_total, sham_idx))
    # StimIdx = stim_idx_total
    if device_type == 'X7':
        stim_indicator = np.asarray(stim_idx_total * 50).astype(np.int64)
        sham_indicator = np.asarray(sham_idx_total * 50).astype(np.int64)
    elif device_type == 'X8':
        stim_indicator = np.asarray(stim_idx_total).astype(np.int64)
        sham_indicator = np.asarray(sham_idx_total).astype(np.int64)

    subplot_count = 3
    fig_height = 5 + 2 + 10
    height_ratio = (np.array([5, 2, 10])).tolist()

    # fig, ax = plt.subplots(subplot_count, 1, figsize=(16, fig_height), height_ratio=height_ratio)
    fig = plt.figure(figsize=(20, fig_height))
    gs = gridspec.GridSpec(subplot_count, 1, height_ratios=height_ratio)

    ax_1 = fig.add_subplot(gs[0, 0])
    t = plot_spectrogram_with_label_points(ax_1, eeg, start_time, sf_eeg)
    ax_2 = fig.add_subplot(gs[1, 0])
    plot_points_distribution(ax_2, t, start_time, stim_points=stim_indicator, sham_points=sham_indicator)
    ax_3 = fig.add_subplot(gs[2, 0])
    plot_stim_vs_sham(ax_3, eeg, sf_eeg, stim_indicator, sham_indicator)
    fig.suptitle('STIM & SHAM', fontsize=25)


    if savefig is not None:
        plt.savefig(savefig, dpi=300, bbox_inches='tight')
