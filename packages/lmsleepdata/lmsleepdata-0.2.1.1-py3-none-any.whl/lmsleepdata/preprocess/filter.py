import scipy.signal as signal
from scipy.io import loadmat


def eeg_filter(eeg, sf_eeg, highpass, highpass_order, lowpass, lowpass_order, bandstop, bandstop_order):
    """
    滤波器实现
    :param eeg: 滤波前的eeg数据
    :param sf_eeg: eeg采样率
    :param highpass: 高通滤波
    :param highpass_order: 高通滤波阶数
    :param lowpass: 低通滤波
    :param lowpass_order: 低通滤波阶数
    :param bandstop: 带阻滤波集合
    :param bandstop_order: 带阻滤波阶数
    :return:
    """
    if bandstop is not None:
        bandstop_count = len(bandstop)
        for i in range(bandstop_count):
            w0_b = bandstop[i][0] / (sf_eeg / 2)
            w1_b = bandstop[i][1] / (sf_eeg / 2)
            b_b, a_b = signal.butter(bandstop_order, [w0_b, w1_b], btype='bandstop', analog=False)
            zi_b = signal.lfilter_zi(b_b, a_b)

            # eeg, _ = signal.lfilter(b=b_b, a=a_b, x=eeg, zi=zi_b)
            eeg= signal.lfilter(b=b_b, a=a_b, x=eeg)
    if highpass is not None:
        wn_h = 2 * highpass / sf_eeg
        b_h, a_h = signal.butter(highpass_order, wn_h, 'highpass', analog=False)
        zi_h = signal.lfilter_zi(b_h, a_h)

        # eeg, _ = signal.lfilter(b_h, a_h, eeg, zi=zi_h)
        eeg= signal.lfilter(b_h, a_h, eeg)
    if lowpass is not None:
        wn_l = 2 * lowpass / sf_eeg
        b_l, a_l = signal.butter(lowpass_order, wn_l, 'lowpass', analog=False)
        zi_l = signal.lfilter_zi(b_l, a_l)

        # eeg, _ = signal.lfilter(b_l, a_l, eeg, zi=zi_l)
        eeg= signal.lfilter(b_l, a_l, eeg)

    return eeg


if __name__ == '__main__':
    eeg = loadmat(r'E:\githome\lm_datahandler\lm_datahandler\train\6655_1.mat')['eeg'].squeeze()
    w0_b = 49 / (500 / 2)
    w1_b = 51 / (500 / 2)
    b_b, a_b = signal.butter(3, [w0_b, w1_b], btype='bandstop', analog=False)
    zi_b = signal.lfilter_zi(b_b, a_b)
    # eeg = signal.lfilter(b=b_b, a=a_b, x=eeg, zi=zi_b)
    # print(";;;")
    print(zi_b.tolist())
    for i in range(50):
        output, zi_b = signal.lfilter(b=b_b, a=a_b, x=[eeg[i]], zi=zi_b)
        print("output: {}, zi_b: {}".format(output, zi_b.tolist()))


