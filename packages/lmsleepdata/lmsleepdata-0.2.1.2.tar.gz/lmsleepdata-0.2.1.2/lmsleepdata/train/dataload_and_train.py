from datetime import datetime

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from lightgbm import LGBMClassifier
import lightgbm as lgb
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split


def generate_dataset(data_path):
    df = pd.read_parquet(data_path)
    df = df.reset_index(drop=True)

    # 去掉不需要的类别，如佩戴异常类别，没有需要去掉的类别，则将下面两行注释掉
    # 由于前面在生成数据集时已经去掉了佩戴异常的类别，这里就不需要了
    # df = df.drop(df[df['stage'] == 6].index)
    # df = df.reset_index(drop=True)

    cols_all = df.columns

    cols_x = cols_all[~cols_all.str.startswith("stage")].tolist()

    X = df[cols_x]
    y = df['stage']

    return X, y


def train(train_data_path, validate_data_path, train_params, class_label, class_weight, model_name):

    X_train, y_train = generate_dataset(train_data_path)
    if validate_data_path is not None:
        X_test, y_test = generate_dataset(validate_data_path)


    y_train.replace(class_label, inplace=True)
    train_params['class_weight'] = class_weight


    clf = LGBMClassifier(**train_params)

    # validate_data_path 不为None时，使用validate_data_path指定的数据集作为验证集
    # validate_data_path 为None时，使用训练集中随机10%的样本作为验证集
    if validate_data_path is not None:
        clf.fit(X_train, y_train, eval_set=(X_test, y_test), eval_metric=['logloss'])
        acccurancy = accuracy_score(y_test, clf.predict(X_test))
        f1 = f1_score(y_test, clf.predict(X_test), average='weighted')
        print(f'Eval set: P: {acccurancy}, F1" {f1}.')
        lgb.plot_metric(clf.evals_result_, metric='multi_logloss')
    else:
        X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, random_state=104, test_size=0.1,
                                                            shuffle=True)
        clf.fit(X_train, y_train, eval_set=(X_test, y_test), eval_metric=['logloss'])
        acccurancy = accuracy_score(y_test, clf.predict(X_test))
        f1 = f1_score(y_test, clf.predict(X_test), average='weighted')
        print(f'Eval set: P: {acccurancy}, F1" {f1}.')
        lgb.plot_metric(clf.evals_result_, metric='multi_logloss')

    print("training accuracy: %.3f" % (clf.score(X_train, y_train)))

    # 保存模型文件
    outdir = "./models/"
    with open('model_name.txt', 'a') as f:
        f.write(outdir + model_name)
        f.write('\n')
    fname = outdir + model_name
    clf.booster_.save_model(fname)

    df_imp = pd.Series(clf.feature_importances_, index=clf.feature_name_, name='Importance').round()
    df_imp.sort_values(ascending=False, inplace=True)
    df_imp.index.name = 'Features'
    df_imp.to_csv(fname[:-4] + ".csv")

    plt.show()
