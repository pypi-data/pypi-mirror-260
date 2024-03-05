import os
from lm_datahandler.data_download.data_download import download_lm_data_from_server

"""
1. paradigms/phones/macs/serviceVersion/sleepScores/stopTypes等参数，为None时表示不做筛选，要筛选时使用[]数组装入要筛选的值
2. save_path表示数据保存的路径，下载好的多套数据会存在该路径下，以每套数据一个文件夹的形式进行保存
"""
start_day = '20231130'
end_day = '20231130'
download_param = {
    # 正式服：http://8.136.42.241/， 测试服：http://150.158.153.12/
    'url': 'http://8.136.42.241:38083/inner/filter',
    # 刺激范式：1. 手动刺激，2. 音频刺激，3. N3闭环刺激，4. 纯记录模式，5. 记录模式， 6. 音频刺激
    'paradigms': None,
    # 用户手机号:
    'phones': [15777799719],
    # 基座mac
    'macs': None,
    # 服务版本
    'serviceVersions': None,
    # 睡眠主观评分，1~5，-1表示未评分
    'sleepScores': None,
    # 停止类型， 0. 断连超时, 1. 用户手动, 2. 头贴放到基座上停止, 3. 关机指令触发, 4. 低电量, 5. 崩溃
    'stopTypes': None,
    # 时间范围，以停止记录的日期为准
    'dateRange': [str(start_day), str(end_day)],
    # 数据时长范围
    'dataLengthRange': [60 * 3 * 60, 60 * 12 * 60],
    # 翻身次数范围
    'turnoverCountRange': None,
    # 刺激次数范围
    'stimulationCountRange': None,
    # 下载保存路径
    'save_path': os.path.join('E:/dataset/x7_tail', "{}_{}".format(start_day, end_day)),
}

data_save_path = download_param["save_path"]
data_list = download_lm_data_from_server(download_param, data_save_path)
