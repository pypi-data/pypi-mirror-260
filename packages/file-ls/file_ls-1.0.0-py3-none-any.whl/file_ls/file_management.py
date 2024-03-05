# -*- coding: utf-8 -*-
from natsort import ns, natsorted
import os

#查找文件夹下所有文件路径及文件名称
def file_ls(path,isrfp=False):
    """
    :param path:文件夹路径
    :param isrfp:是否返回文件名，默认为False,只返回文件路径，True返回文件名称
    """
    file_list = os.listdir(path)
    file_list = natsorted(file_list, alg=ns.PATH)
    if isrfp:
        return [(file, os.path.join(path, file)) for file in file_list]
    return [(os.path.join(path, file)) for file in file_list]