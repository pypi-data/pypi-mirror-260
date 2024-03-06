#! /usr/bin/env python
# -*- coding: utf-8 -*-
__all__ = ('time_stamp', 'load_pkl', 'save_pkl', 'load_json', 'save_json', 'calculate_str_similarity',
           'save_list2txt', 'load_txt2list',
           'read_excel_with_header', 'prename_from_abs_path', 'name_from_abs_path',
           'mkdir', 'rmdir', 'clear_mkdir', 'check_command', 'filter_df_column_with_list', 'pd_column_to_list',
           'plain_logger')

import difflib
import errno
import json
import logging
import os
import pickle as pkl
from shutil import rmtree
from time import strftime
import pandas as pd


def time_stamp():
    """时间戳：年月日时分"""
    return strftime('%Y%m%d%H%M%S')


def load_pkl(path):
    with open(path, 'rb') as f:
        pkl_file = pkl.load(f)
    return pkl_file


def save_pkl(pkl_file, path):
    with open(path, 'wb') as f:
        pkl.dump(pkl_file, f)


def load_json(path):
    with open(path, 'r') as f:
        json_file = json.load(f)
    return json_file


def save_json(json_file, path):
    json.dump(json_file, open(path, 'w'))


def calculate_str_similarity(str1, str2):
    """检测两个字符串有多相似"""
    seq = difflib.SequenceMatcher(None, str1, str2)
    return seq.ratio()


def load_txt2list(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return [line.strip() for line in lines]


def save_list2txt(content_list, txt_path):
    """将list内容写入txt，每个元素之间换行"""
    with open(txt_path, 'w') as f:
        for content_i in content_list:
            f.write(content_i)
            f.write('\n')


def read_excel_with_header(file_path, header=0):
    """header是列名，=0表示首行是各项，=1表示第二行是各项，=[0, 1]表示前两行都是"""
    df = pd.read_excel(file_path, header=header)
    return df


def split_list_into_n_lists(primary_list, n):
    """将primary_list n 尽可能等分，返回一个含有n个列表的列表"""
    primary_length = len(primary_list)
    assert primary_length > n
    length_n, reminder = divmod(primary_length, n)  # 基本长度和余数
    list_of_lists = []
    start = 0
    for i in range(n):
        if i < reminder:
            end = start + length_n + 1
        else:
            end = start + length_n
        list_i = list(primary_list[start:end])
        list_of_lists.append(list_i)
        start = end
    return list_of_lists


def prename_from_abs_path(path):
    """从绝对路径获取文件名"""
    name = os.path.split(path)[1]
    prename = os.path.splitext(name)[0]
    return prename


def name_from_abs_path(path):
    """从绝对路径获取带有后缀的文件名"""
    name = os.path.split(path)[1]
    return name


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def rmdir(path):
    """递归删除，path所指的文件夹也删除"""
    try:
        rmtree(path)
    except:
        pass


def clear_mkdir(path):
    """更新建立文件夹"""
    rmdir(path)
    mkdir(path)


def check_command(command):
    """对有问题的命令进行调整"""
    focus_chars = ['(', ')']
    for focus_char in focus_chars:
        valid_statement = '\\' + focus_char
        # print(valid_statement)
        if (focus_char in command) and (valid_statement not in command):
            command = command.replace(focus_char, valid_statement)
    return command


def filter_df_column_with_list(df, column_name, filter_list):
    """过滤得到新的df，要求column_name这一列的内容在filter_list里面"""
    df_wanted = df[df[column_name].isin(filter_list)]
    return df_wanted


def pd_column_to_list(df, column_name):
    return df[column_name].values.tolist()


def plain_logger(log_path, log_name):
    """init logger"""
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename=log_path, level=logging.INFO, filemode='w', format=LOG_FORMAT)
    logger = logging.getLogger(log_name)
    return logger
