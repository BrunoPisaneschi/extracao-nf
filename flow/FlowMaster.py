# -*- coding:utf-8 -*-
# /usr/bin/python3

import base64
import glob
import os
import random
import string
from datetime import datetime
from os import path, makedirs, remove
import re
import requests
from utils.Pipefy import Pipefy
from utils.ExcelUtils import excel
from utils.PdfUtils import read_pdf
from utils.FindLocationNf import find_data


class pipefy():
    def __init__(self, token):
        self._token = token
        self._pipe_id = 1201770
        self._dict_datas = {}

    def extract_datas(self):
        self._clear_dir()
        _pipefy = Pipefy(self._token)
        _pipes = _pipefy.pipes([self._pipe_id])[0]
        _count = 1
        for _cards in _pipes['phases']:
            if 'notas recebidas' in _cards['name'].lower():
                for _edge in _cards['cards']['edges']:
                    self._dict_datas[_count] = {}
                    _infos_card = _pipefy.card(_edge['node']['id'])
                    for _fields in _infos_card['fields']:
                        if ('arquivo da nota fiscal' in _fields['name'].lower()):
                            _files_list = _fields['value'].strip().split(",")
                            for _file_list in _files_list:
                                if (".pdf" in _file_list):
                                    _link_pdf = re.sub(r'[\[\]\\"]', '', _file_list.strip())
                                    print("NF: {}".format(_link_pdf))
                                    self._dict_datas[_count].update({'link_pdf': _link_pdf})
                                    _nf_name = self._generate_nf_name() + ".pdf"
                                    print("Nome Arquivo NF: {}".format(_nf_name))
                                    self._get_base64_curriculo(_link_pdf, _nf_name)
                                    self._dict_datas[_count].update({'caminho_pdf': '.\\anexos\\' + _nf_name})
                                    break
                    print("-" * 20)
                    _count += 1
        return self._dict_datas

    def _get_base64_curriculo(self, _string_link, _nome_pdf):
        _headers = {'Content-Type': 'text/plain'}
        response = requests.get(_string_link)
        _caminho_curriculo = '.\\anexos\\' + _nome_pdf
        if (not path.exists(r'.\anexos')):
            makedirs(r'.\anexos')
        _file = open(_caminho_curriculo, 'wb')
        _file.write(response.content)
        _file.close()
        _data = open(_caminho_curriculo, "rb").read()
        _base64 = base64.b64encode(_data).decode("utf-8")
        return _base64

    def _generate_nf_name(self):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(8))
        return result_str

    def _clear_dir(self):
        dir = r'.\anexos'
        if path.exists(dir):
            files = glob.glob(dir + '\\*')
            for f in files:
                os.remove(f)


class datas_nf:
    def __init__(self, _dict_datas):
        self._dict_datas = _dict_datas
        self._excel_utils = excel()
        self._excel_file = ".\\relatorio\\" + datetime.today().strftime("%m-%Y") + " - ExtracaoNFs.xlsx"

    def find_datas_nf(self):
        for _index, _data in self._dict_datas.items():
            print(_data['caminho_pdf'])
            try:
                _text_pdf = read_pdf(_data['caminho_pdf'])
                if (_text_pdf is None):
                    _text_pdf = ""
                else:
                    _text_pdf.strip()
                _find_data(_data, _text_pdf)
            except:
                _data.update({'valor': 'informacao nao encontrada'})
                _data.update({'nome': 'informacao nao encontrada'})
                _data.update({'mes_vigente': 'informacao nao encontrada'})

        if not path.exists(".\\relatorio\\"):
            os.makedirs(".\\relatorio\\")

        if path.exists(self._excel_file):
            self._excel_utils.update_excel(self._dict_datas)
        else:
            self._excel_utils.write_excel(self._dict_datas)
