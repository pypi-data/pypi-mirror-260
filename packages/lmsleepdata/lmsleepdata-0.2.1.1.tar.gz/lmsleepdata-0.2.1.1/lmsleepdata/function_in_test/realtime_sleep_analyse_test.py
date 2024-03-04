import time
from datetime import datetime
import redis
import os
import requests
import json

def test():
    """
    用于X8后台分期方案的本地测试
    :return:
    """
    r = redis.Redis(host='localhost', port=6379, db=0)
    zx = r.get('zx')
    data_path = r"E:\dataset\dev_test_data\4649_X8"
    eeg_file_data = open(os.path.join(data_path, "eeg.eeg"), 'rb')
    acc_file_data = open(os.path.join(data_path, "acc.acc"), 'rb')

    eeg_bytes = eeg_file_data.read()
    acc_bytes = acc_file_data.read()

    eeg_package = list(eeg_bytes)[534:]
    acc_package = list(acc_bytes)[534:]

    epoch = 2000

    id = "4649"
    for i in range(epoch):
        i = i
        eeg_i = eeg_package[i * 218 * 10 * 15:(i + 1) * 218 * 10 * 15]
        acc_i = acc_package[i * 48 * 10 * 15:(i + 1) * 48 * 10 * 15]
        eeg_i.extend(acc_i)
        data_i = eeg_i
        data_bytes_i = bytes(data_i)

        data_key = 'record:cache:{}'.format(id)
        data_time = int(datetime.now().timestamp() * 1000)
        split = [218 * 10 * 15, 48 * 10 * 15]

        r.delete(data_key)

        r.set(data_key, data_bytes_i, ex=60)

        download_url = 'http://localhost:5000/online_sleep_analysis_by_epoch'
        params = {
            'id': id,
            'split': split,
            'time': data_time,
            'data_key': data_key
        }
        before_time = datetime.now().timestamp()
        post_response = requests.post(download_url, json=json.dumps(params))

        result_url = 'http://localhost:5000/get_online_sleep_staging_res_by_id'
        params = {
            'id': id
        }
        get_response = requests.get(result_url, params=params)
        end_time = datetime.now().timestamp()
        print("Time cost: {}, epoch {}: {}, sleep staging result: {}".format(end_time - before_time, i,
                                                                             post_response.text, get_response.text))
        time.sleep(5)


if __name__ == '__main__':
    test()
