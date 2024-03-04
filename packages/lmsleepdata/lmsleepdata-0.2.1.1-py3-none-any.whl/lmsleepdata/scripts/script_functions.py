import os.path
import sys
import numpy as np
import lightgbm as lgb
import scipy.signal as sp_sig
from scipy import signal
from scipy.integrate._quadrature import simps
from scipy.io import loadmat

from lmsleepdata.data_download.data_download import download_lm_data_from_server
from lmsleepdata.datahandler import DataHandler
import pandas as pd

from lmsleepdata.function_in_test.other_features import generate_cluster_feature1, generate_cluster_feature2, \
    generate_cluster_feature3



def download_and_full_analyse(download_params, analyse_param=None):
    data_save_path = download_params["save_path"]
    data_list = download_lm_data_from_server(download_params, data_save_path)

    analysis_save_path = download_params["analysis_save_path"]

    local_datas_full_analyse(data_save_path, data_list, analysis_save_path=analysis_save_path,
                             analyse_param=analyse_param)


def local_datas_full_analyse(data_path, data_names, analysis_save_path=None, analyse_param=None):
    assert os.path.exists(data_path), "The input dir path does not exist."

    if analyse_param is None:
        device_type = 'X7'
        data_type = "sleep"
        pre_process_param = {'highpass': 0.5, 'lowpass': None, 'bandstop': [[49, 51]]},
        sleep_staging_param = {'use_acc': False, 'use_time': False, 'staging_mode': 'offline'},
        parse_to_mat = True
        save_features = True
        slow_wave_detect = False
        spindle_detect = False
        show_plots = False
        plot_sw_stim_sham = True
        plot_sleep_fig = True
    else:
        device_type = analyse_param['device_type']
        data_type = analyse_param["data_type"]
        pre_process_param = analyse_param["pre_process_param"]
        sleep_staging_param = analyse_param["sleep_staging_param"]
        parse_to_mat = analyse_param["parse_to_mat"]
        save_features = analyse_param["save_features"]
        slow_wave_detect = analyse_param["slow_wave_detect"]
        spindle_detect = analyse_param["spindle_detect"]
        show_plots = analyse_param["show_plots"]
        plot_sw_stim_sham = analyse_param["plot_sw_stim_sham"]
        plot_sleep_fig = analyse_param["plot_sleep_fig"]

    if analysis_save_path is None:
        analysis_save_path = data_path
    else:
        if not os.path.exists(analysis_save_path):
            os.mkdir(analysis_save_path)
    if data_names is None:
        data_names = os.listdir(data_path)
    for i, data_name in enumerate(data_names):
        print("Start analysis data: {}".format(data_name))
        if not (os.path.exists(os.path.join(data_path, data_name + "/eeg.eeg")) or os.path.exists(
                os.path.join(data_path, data_name + "/eeg.qle"))):
            print("data: \"{}\" not found, skipped.".format(data_name))
            continue
        try:

            data_handler = DataHandler()

            temp_data_path = os.path.join(data_path, data_name)

            data_analysis_save_path = os.path.join(analysis_save_path, data_name)

            if not os.path.exists(data_analysis_save_path):
                os.mkdir(data_analysis_save_path)
            sleep_fig_save_path = os.path.join(data_analysis_save_path, "sleep_fig.png")

            data_preview_png_save_path = os.path.join(data_analysis_save_path, "data_preview.png")

            slow_wave_stim_sham_plot = os.path.join(data_analysis_save_path, "sw_stim_sham_fig.png")

            analysis_results_save_path = os.path.join(data_analysis_save_path, "analysis_results.xlsx")

            analysis_report_save_path = os.path.join(data_analysis_save_path, data_name + "_sleep_report.pdf")

            data_preview_save_path = os.path.join(data_analysis_save_path, data_name + "_data_preview.pdf")

            features_save_path = os.path.join(data_analysis_save_path, "features.parquet")

            # 数据加载
            patient_info = {"phone_number": data_name[0:11]}
            data_handler.load_data(device_type=device_type, data_name=data_name, data_path=temp_data_path,
                                   patient_info=patient_info)
            if parse_to_mat:
                data_handler.save_data_to_mat(os.path.join(data_analysis_save_path, "eeg_and_acc.mat"))

            if data_type == "sleep":
                # 绘制慢波增强对比图，并保存
                if plot_sw_stim_sham:
                    data_handler.plot_sw_stim_sham(savefig=slow_wave_stim_sham_plot)

                # 进行睡眠分期，计算睡眠指标，绘制睡眠综合情况图，并保存
                data_handler.preprocess(filter_param=pre_process_param)
                data_handler.sleep_staging_with_internal_model(sleep_staging_param['use_acc'],
                                                               sleep_staging_param['use_time'],
                                                               sleep_staging_param['staging_mode'])
                data_handler.compute_sleep_variables()

                if save_features:
                    data_handler.save_features_to_parquet(features_save_path)

                if plot_sleep_fig:
                    data_handler.plot_sleep_data(savefig=sleep_fig_save_path)
                    data_handler.plot_data_preview(savefig=data_preview_png_save_path)

                # spindle检测和慢波检测
                if slow_wave_detect:
                    data_handler.sw_detect()
                if spindle_detect:
                    data_handler.spindle_detect()

                # data_handler.plot_sp_results_by_id(60, range=5000, savefig=os.path.join(data_analysis_save_path, "sp_no.{}.png".format(50)))
                # data_handler.plot_sw_results_by_id(50, range=5000, savefig=os.path.join(data_analysis_save_path, "sw_no.{}.png".format(50)))

                # 导出结果成excel
                data_handler.export_analysis_result_to_xlsx(analysis_results_save_path, sw_results=slow_wave_detect,
                                                            sp_results=spindle_detect,
                                                            sleep_variables=True)
            elif data_type == "anes":
                # 进行睡眠分期，计算睡眠指标，绘制睡眠综合情况图，并保存
                data_handler.preprocess(filter_param={'highpass': 0.5, 'lowpass': None, 'bandstop': [
                    [49, 51]]}).sleep_staging_with_internal_model(
                    use_acc=True).compute_sleep_variables().plot_anes_data(
                    savefig=sleep_fig_save_path)

            if show_plots:
                data_handler.show_plots()

            data_handler.export_analysis_report(analysis_report_save_path)
            data_handler.export_data_preview(data_preview_save_path)


        except AssertionError as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("AssertionError: {}".format(e))
            print("File: {}".format(exc_traceback.tb_frame.f_code.co_filename))
            print("Line Number: {}".format(exc_traceback.tb_lineno))
            print("当前数据出错，将跳过当前数据.")
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("Unknown Error: {}".format(e))
            print("File: {}".format(exc_traceback.tb_frame.f_code.co_filename))
            print("Line Number: {}".format(exc_traceback.tb_lineno))
            print("当前数据出错，将跳过当前数据.")
        finally:

            continue


def local_data_concat_and_analyse(data_path, data_names, analysis_save_path=None, analyse_param=None):
    assert os.path.exists(data_path), "The input dir path does not exist."

    if analyse_param is None:
        data_type = "sleep"
        pre_process_param = {'highpass': 0.5, 'lowpass': None, 'bandstop': [[49, 51]]},
        parse_to_mat = True
        show_plots = False
        plot_sw_stim_sham = True
        plot_sleep_fig = True
    else:
        data_type = analyse_param["data_type"]
        pre_process_param = analyse_param["pre_process_param"]
        parse_to_mat = analyse_param["parse_to_mat"]
        show_plots = analyse_param["show_plots"]
        plot_sw_stim_sham = analyse_param["plot_sw_stim_sham"]
        plot_sleep_fig = analyse_param["plot_sleep_fig"]

    data_handler = DataHandler()

    for i in range(len(data_names)):
        # 数据加载
        if i == 0:
            patient_info = {"phone_number": data_names[i][0:11]}
            data_handler.load_data(data_name=data_names[0], data_path=os.path.join(data_path, data_names[i]),
                                   patient_info=patient_info)
        else:
            data_handler.concat_data(data_path=os.path.join(data_path, data_names[i]))

    data_name = data_handler.data_name

    data_analysis_save_path = os.path.join(analysis_save_path, data_name)

    if not os.path.exists(data_analysis_save_path):
        os.mkdir(data_analysis_save_path)
    sleep_fig_save_path = os.path.join(data_analysis_save_path, "sleep_fig.png")
    slow_wave_stim_sham_plot = os.path.join(data_analysis_save_path, "sw_stim_sham_fig.png")

    analysis_results_save_path = os.path.join(data_analysis_save_path, "analysis_results.xlsx")

    analysis_report_save_path = os.path.join(data_analysis_save_path, "sleep_report.pdf")

    if parse_to_mat:
        data_handler.save_data_to_mat(os.path.join(data_analysis_save_path, "eeg_and_acc.mat"))

    if data_type == "sleep":
        # 绘制慢波增强对比图，并保存
        if plot_sw_stim_sham:
            data_handler.plot_sw_stim_sham(savefig=slow_wave_stim_sham_plot)

        # 进行睡眠分期，计算睡眠指标，绘制睡眠综合情况图，并保存
        data_handler.preprocess(filter_param=pre_process_param).sleep_staging_with_internal_model(use_acc=True)
        # if os.path.exists(os.path.join(temp_data_path, "hypno.mat")):
        #     hypno = loadmat(os.path.join(temp_data_path, "hypno.mat"))["manual"]
        #     data_handler.sleep_staging_result = np.squeeze(hypno)
        data_handler.compute_sleep_variables()

        if plot_sleep_fig:
            data_handler.plot_sleep_data(savefig=sleep_fig_save_path)


        # spindle检测和慢波检测
        data_handler.sw_detect()
        data_handler.spindle_detect()

        # 导出结果成excel
        data_handler.export_analysis_result_to_xlsx(analysis_results_save_path, sw_results=True,
                                                    sp_results=True,
                                                    sleep_variables=True)
    elif data_type == "anes":
        # 进行睡眠分期，计算睡眠指标，绘制睡眠综合情况图，并保存
        data_handler.preprocess(filter_param={'highpass': 0.5, 'lowpass': None, 'bandstop': [
            [49, 51]]}).sleep_staging_with_internal_model().compute_sleep_variables().plot_anes_data(
            savefig=sleep_fig_save_path)

    if show_plots:
        data_handler.show_plots()

    data_handler.export_analysis_report(analysis_report_save_path)




def compute_sleep_variables_from_hypno(hypno):
    data_handler = DataHandler()
    data_handler.compute_sleep_variables(hypno)
    sleep_variables_df = {
        "TST(H)": [data_handler.sleep_variables["TST"] / 3600],
        "SOL(H)": [data_handler.sleep_variables["SOL"] / 3600],
        "GU(H)": [data_handler.sleep_variables["GU"] / 3600],
        "WASO(M)": [data_handler.sleep_variables["WASO"] / 60],
        "SE(%)": [data_handler.sleep_variables["SE"] * 100],
        "AR": [data_handler.sleep_variables["AR"]],
        "N3(H)": [data_handler.sleep_variables["N3"] / 3600],
        "N12(H)": [data_handler.sleep_variables["N12"] / 3600],
        "REM(H)": [data_handler.sleep_variables["REM"] / 3600],
        "Hypno": [data_handler.sleep_variables["HYPNO"]]
    }
    print(sleep_variables_df)


def bandpower_from_psd_ndarray(bands, psd, freqs, relative=True):
    # Type checks
    assert isinstance(bands, list), "bands must be a list of tuple(s)"
    assert isinstance(relative, bool), "relative must be a boolean"

    # Safety checks
    freqs = np.asarray(freqs)
    psd = np.asarray(psd)
    assert freqs.ndim == 1, "freqs must be a 1-D array of shape (n_freqs,)"
    assert psd.shape[-1] == freqs.shape[-1], "n_freqs must be last axis of psd"

    # Extract frequencies of interest
    all_freqs = np.hstack([[b[0], b[1]] for b in bands])
    fmin, fmax = min(all_freqs), max(all_freqs)
    idx_good_freq = np.logical_and(freqs >= fmin, freqs <= fmax)
    freqs = freqs[idx_good_freq]
    res = freqs[1] - freqs[0]

    # Trim PSD to frequencies of interest
    psd = psd[..., idx_good_freq]

    # plt.imshow(psd.T[:50,:], cmap='jet')
    # plt.show()
    # assert 0

    # Check if there are negative values in PSD
    if (psd < 0).any():
        pass

    # Calculate total power
    total_power = simps(psd, dx=res, axis=-1)
    total_power = total_power[np.newaxis, ...]

    # Initialize empty array
    bp = np.zeros((len(bands), *psd.shape[:-1]), dtype=np.float64)

    # Enumerate over the frequency bands
    labels = []
    for i, band in enumerate(bands):
        b0, b1, la = band
        labels.append(la)
        idx_band = np.logical_and(freqs >= b0, freqs <= b1)
        bp[i] = simps(psd[..., idx_band], dx=res, axis=-1)

    if relative:
        bp /= total_power

    all_freqs = all_freqs.reshape(-1, 2)
    total_bands = all_freqs[:, 1] - all_freqs[:, 0]
    total_bands = total_bands[..., np.newaxis]
    bp /= total_bands
    return bp