import os
from lmsleepdata.scripts.script_functions import download_and_full_analyse

"""
1. paradigms/phones/macs/serviceVersion/sleepScores/stopTypes等参数，为None时表示不做筛选，要筛选时使用[]数组装入要筛选的值
2. save_path表示数据保存的路径，下载好的多套数据会存在该路径下，以每套数据一个文件夹的形式进行保存
3. analysis_save_path表示分析结果的保存路径，以每套数据的分析结果一个文件夹的形式进行保存
   analysis_save_path与save_path一致则直接保存在原数据文件夹
"""

start_day = '20231201'
end_day = '20240111'
download_param = {
    # 正式服：http://8.136.42.241/， 测试服：http://150.158.153.12/
    'url': 'http://150.158.153.12:38083/inner/filter',
    # 刺激范式：1. 手动刺激，2. 音频刺激，3. N3闭环刺激，4. 纯记录模式，5. 记录模式， 6. 音频刺激
    'paradigms': None,
    # 用户手机号
    'phones': [13547951033],
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
    'save_path': os.path.join('E:/dataset/x7_data_by_days/data', "{}_{}".format(start_day, end_day)),
    # 分析结果保存路径（为None表示保存在数据下载路径中）
    'analysis_save_path': os.path.join('E:/dataset/x7_data_by_days/analysis', "{}_{}".format(start_day, end_day)),
}
analyse_param = {
    # 设备类型：X7/X8
    'device_type': "X8",
    # 数据类型：sleep(睡眠数据) / anes(麻醉数据)
    'data_type': "sleep",
    # 滤波参数，一般不需要改动
    'pre_process_param': {'highpass': 0.5, 'lowpass': None, 'bandstop': [[49, 51]]},
    # 分期参数：1.是否使用体动特征；2.是否使用时间特征；3.分期模式（实时/非实时）
    'sleep_staging_param': {'use_acc': False, 'use_time': False, 'staging_mode': 'offline'},
    # 是否额外保存数据成.mat格式
    'parse_to_mat': True,
    # 是否进行丢包补充和断连补充
    'do_padding': False,
    # 是否额外保存特征到.parquet格式
    'save_features': True,
    # 是否进行慢波检测
    'slow_wave_detect': False,
    # 是否进行Spindle检测
    'spindle_detect': False,
    # 是否显示matplotlib绘图，一般不推荐
    'show_plots': False,
    # 是否绘制慢波增强对比图(ERP图)
    'plot_sw_stim_sham': True,
    # 是否绘制睡眠分期图
    'plot_sleep_fig': True
}

# 在线下载并分析
download_and_full_analyse(download_param, analyse_param)
