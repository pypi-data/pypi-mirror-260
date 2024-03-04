from lmsleepdata.train.sleepyco_net import MainModel
import torch
import scipy
import numpy as np
"""
指定数据的采样频率，为未处理的eeg数据进行睡眠分期
"""


def predict_with_raw_eeg(raw_eeg: np.ndarray, sf: int) -> np.ndarray:
    eeg = (raw_eeg - 32767) / 65536 * 2.5 * 1000 * 1000 / 100
    cut: int = int(eeg.shape[0] / (30 * sf)) * (30 * sf)
    eeg = eeg[:cut]
    eeg = eeg.reshape(-1, 30 * sf)
    resample_eeg = scipy.signal.resample(eeg, 250 * 30, axis=1)  # 重采样成250Hz
    net = MainModel()
    net.eval()
    state_dict = torch.load(r'../models/sleepyco_people_model.pth', map_location=torch.device('cpu'))
    new_state_dict = {}
    for k, v in state_dict.items():
        name = k.replace('module.', '')
        new_state_dict[name] = v
    net.load_state_dict(new_state_dict)
    result = []
    net.eval()
    for i in range(resample_eeg.shape[0]):
        if i < 10:
            input = torch.from_numpy(resample_eeg[:i + 1, :]).float()
        else:
            input = torch.from_numpy(resample_eeg[i - 10:i, :]).float()

        input = input.reshape(1, 1, -1)

        outputs = net(input)
        outputs_sum = torch.zeros_like(outputs[0])

        for j in range(len(outputs)):
            outputs_sum += outputs[j]
        predicted = torch.argmax(outputs_sum, 1)
        result.append(predicted.item())
    result = [x for x in result for _ in range(2)]  # 列表推导式， 把result中的每个值复制一次
    stage_trans_dict = {
        0: 3,
        1: 1,
        2: 1,
        3: 0,
        4: 2
    }
    transformed_result = [stage_trans_dict.get(x, x) for x in result]


    return np.array(transformed_result)
