from lmsleepdata.scripts.script_functions import local_datas_full_analyse

analyse_param = {
    # 设备类型：X7/X8
    'device_type': "X8",
    # 数据类型：sleep(睡眠数据) / anes(麻醉数据)
    'data_type': "sleep",
    # 滤波参数，一般不需要改动
    'pre_process_param': {'highpass': 0.5, 'lowpass': None, 'bandstop': [[49, 51]]},
    # 分期参数：1.是否使用体动特征；2.是否使用时间特征；3.分期模式（实时/非实时）
    'sleep_staging_param': {'use_acc': False, 'use_time': False, 'staging_mode': 'realtime'},
    # 是否额外保存数据成.mat格式
    'parse_to_mat': True,
    # 是否进行丢包补充和断连补充
    'do_padding': False,
    # 是否额外保存特征到.parquet格式
    'save_features': False,
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

"""
data_path: 表示待分析数据（一套一文件夹形式）的存放路径
data_names：表示待分析数据列表，为None则分析data_path中的所有数据
analysis_save_path： 表示分析结果的保存路径
"""
local_datas_full_analyse(data_path=r'E:\dataset\dev_test_data',
                         data_names=[
                             "19101612301_0219-22_16_21_0220-07_04_57_0.00_4",
                         ],
                         analysis_save_path=r'E:\dataset\dev_test_data', analyse_param=analyse_param)
