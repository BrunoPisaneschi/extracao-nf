# -*- coding:utf-8 -*-
# !/usr/bin/python3

from flow.FlowMaster import pipefy, datas_nf

if __name__ == '__main__':
    token = ""
    pipefy = pipefy(token)
    dict_data = pipefy.extract_datas()
    nfs = datas_nf(dict_data)
    nfs.find_datas_nf()
