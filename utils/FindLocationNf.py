import os
import re
from utils.OcrNota import *

def find_data(_dict_data, _text_pdf):
    ## valida qual prefeitura está sendo lida
    if ('PREFEITURA DE APARECIDA DE GOIÂNIA' in _text_pdf.upper()):
        ## captura valor da nota
        _valor_nota = re.findall(r'(?<=NOTA\sFISCAL\sR\$)(.*)', _text_pdf.upper())
        if (len(_valor_nota) > 0):
            _dict_data.update({'valor': _valor_nota[0].strip()})

        ## captura nome do emissor
        _nomes = re.findall(r'(?<=GOV\.BR\s\s)(.*)', _text_pdf.upper())
        for _nome in _nomes:
            if ('' not in _nome):
                ## capturar somente dígitos
                _nome = re.sub('[0-9]', '', _nome).strip()
                _dict_data.update({'nome': _nome})
                break

        ## captura mês vigente
        _mes_vigente = re.findall(r'(?<=NO\sMUNICÍPIO\s\s)(.*?)(?=\s)', _text_pdf.upper())
        if (len(_mes_vigente) > 0):
            _dict_data.update({'mes_vigente': _mes_vigente[0][3:10]})
    elif ('MUNICÍPIO DE ARARAS' in _text_pdf.upper()):
        ## captura valor da nota
        _valor_nota = re.findall(r'(?<=PGDAS-D\sR\$\s)(.*)', _text_pdf.upper())
        if (len(_valor_nota) > 0):
            _dict_data.update({'valor': _valor_nota[0].strip()})

        ## captura nome do emissor
        _nomes = re.findall(r'(?<=\s-\s)(.*?)(?=\sOS\sSERVIÇOS\sCONSTANTES\sNA\sNOTA\sFISCAL)', _text_pdf.upper())
        for _nome in _nomes:
            if ('' not in _nome):
                ## capturar somente dígitos
                _nome = re.sub('[0-9]', '', _nome).strip()
                _dict_data.update({'nome': _nome})
                break

        ## captura mês vigente
        _mes_vigente = re.findall(r'(.*?)(?=\sC\/APRES)', _text_pdf.upper())
        if (len(_mes_vigente) > 0):
            _dict_data.update({'mes_vigente': _mes_vigente[0][3:10]})
    elif ('PREFEITURA MUNICIPAL DE BAURU' in _text_pdf.upper()):
        ## captura valor da nota
        _valor_nota = re.findall(r'(?<=BAURU.\s)(.*)', _text_pdf.upper())
        if (len(_valor_nota) > 0):
            _dict_data.update({'valor': _valor_nota[0].strip()})

        ## captura nome do emissor
        _nomes = re.findall(r'(?<=RAZÃO\sSOCIAL:\s)(.*)', _text_pdf.upper())
        for _nome in _nomes:
            if ('' not in _nome):
                ## capturar somente dígitos
                _nome = re.sub('[0-9]','',_nome).strip()
                _dict_data.update({'nome': _nome})
                break

        ## captura mês vigente
        _mes_vigente = re.findall(r'(?<=EMISSÃO:\s)(.*)', _text_pdf.upper())
        if (len(_mes_vigente) > 0):
            _dict_data.update({'mes_vigente': _mes_vigente[0][3:10]})
    elif ('NOTA CURITIBANA' in _text_pdf.upper()):
        _image_filename = r".\anexos\curitiba"
        _pdf_filename = _dict_data['caminho_pdf']
        _image_ocr = r".\anexos\image_ocr.png"
        basewidth = 360

        convert_pdf_to_image(_pdf_filename, _image_filename)

        cut_image(_image_filename + ".jpg", 3220, 510, 3600, 580, _image_ocr, basewidth)
        _dict_data.update({'mes_vigente': ocr_image(_image_ocr)[3:11]})

        cut_image(_image_filename + ".jpg", 1220, 980, 3500, 1070, _image_ocr, basewidth=488)
        _leitura_emissor = ocr_image(_image_ocr)
        _leitura_emissor = re.sub(r'[0-9]', '', _leitura_emissor).upper().strip()
        _dict_data.update({'nome': _leitura_emissor})

        cut_image(_image_filename + ".jpg", 2335, 3800, 2925, 3880, _image_ocr, basewidth)
        _dict_data.update({'valor': ocr_image(_image_ocr).strip()})

        ## remove files
        os.remove(_image_filename+".jpg")
        os.remove(_image_ocr)
    elif ('PREFEITURA DE GOIÂNIA' in _text_pdf.upper()):
        ## captura valor da nota
        _valor_nota = re.findall(r'(?<=\)VALOR\sDA\sNOTA\sR\$\s)(.*)', _text_pdf.upper())
        if (len(_valor_nota) > 0):
            _dict_data.update({'valor': _valor_nota[0].strip()})

        ## captura nome do emissor
        _nomes = re.findall(r'(?<=RAZÃO\sSOCIAL\s)(.*)', _text_pdf.upper())
        for _nome in _nomes:
            if ('' not in _nome):
                ## capturar somente dígitos
                _nome = re.sub('[0-9]', '', _nome).strip()
                _dict_data.update({'nome': _nome.strip()})
                break

        ## captura mês vigente
        _mes_vigente = re.findall(r'(?<=EMISSÃO\s)(.*)', _text_pdf.upper())
        if (len(_mes_vigente) > 0):
            _dict_data.update({'mes_vigente': _mes_vigente[0][3:10]})
    elif ('MUNICIPIO DE SAO BERNARDO DO CAMPO' in _text_pdf.upper()):
        ## captura valor da nota
        _valor_nota = re.findall(r'(?<=VALOR TOTAL DA NOTA:)(.*?)(.*)', _text_pdf.upper())
        if (len(_valor_nota) > 0):
            if(len(_valor_nota[0])>1):
                _dict_data.update({'valor': _valor_nota[0][1].strip()})

        ## captura nome do emissor
        _nomes = re.findall(r'(?<=NOME\s)(.*?)(.*)', _text_pdf.upper())
        for _nome in _nomes:
            if('' not in _nome[1]):
                _dict_data.update({'nome': _nome[1].strip()})
                break

        ## captura mês vigente
        _mes_vigente = re.findall(r'(?<=DATAEHORADAEMISSÃO)(.*?)(?=COMPETÊNCIA)', re.sub('\s','',_text_pdf.upper()))
        if (len(_mes_vigente) > 0):
            _dict_data.update({'mes_vigente': _mes_vigente[0][3:10]})
    elif('' == _text_pdf.upper() or 'SÃO PAULO' in _text_pdf.upper):
        _image_filename = r".\anexos\sao_paulo"
        _pdf_filename = _dict_data['caminho_pdf']
        _image_ocr = r".\anexos\image_ocr.png"
        basewidth = 360

        convert_pdf_to_image(_pdf_filename, _image_filename)

        cut_image(_image_filename + ".jpg", 3050, 510, 3425, 580, _image_ocr, basewidth)
        _dict_data.update({'mes_vigente': re.sub('[^0-9\/]', '', ocr_image(_image_ocr)[3:11])})

        if (not _dict_data['mes_vigente']):
            cut_image(_image_filename + ".jpg", 2900, 260, 3300, 350, _image_ocr, basewidth)
            _dict_data.update({'mes_vigente': re.sub('[^0-9\/]', '', ocr_image(_image_ocr)[3:11])})
        elif (len(_dict_data['mes_vigente']) > 0) and (len(_dict_data['mes_vigente']) < 7):
            cut_image(_image_filename + ".jpg", 3050, 510, 3480, 680, _image_ocr, basewidth)
            _dict_data.update({'mes_vigente': re.sub('[^0-9\/]', '', ocr_image(_image_ocr)[3:11])})

        cut_image(_image_filename + ".jpg", 920, 910, 2300, 980, _image_ocr, basewidth)
        _leitura_emissor = ocr_image(_image_ocr)
        _leitura_emissor = re.sub(r'[0-9]', '', _leitura_emissor).upper().strip()
        _dict_data.update({'nome': _leitura_emissor})

        if ('TOMADOR' in _dict_data['nome']):
            cut_image(_image_filename + ".jpg", 1030, 640, 2000, 710, _image_ocr, basewidth)
            _leitura_emissor = ocr_image(_image_ocr)
            _leitura_emissor = re.sub(r'[0-9]', '', _leitura_emissor).upper().strip()
            _dict_data.update({'nome': _leitura_emissor})


        cut_image(_image_filename + ".jpg", 2500, 3380, 2925, 3470, _image_ocr, basewidth)
        _dict_data.update({'valor': re.sub(r'[^0-9,.]', '', ocr_image(_image_ocr).strip())})
        if (not _dict_data['valor']):
            cut_image(_image_filename + ".jpg", 2400, 2850, 2825, 2940, _image_ocr, basewidth)
            _dict_data.update({'valor': re.sub(r'[^0-9,.]', '', ocr_image(_image_ocr).strip())})

        ## remove files
        os.remove(_image_filename+".jpg")
        os.remove(_image_ocr)
    elif ('PREFEITURA DO MUNICÍPIO DE TIETÊ' in _text_pdf.upper()):
        ## captura valor da nota
        _valor_nota = re.findall(r'(?<=R\$\s)(.*)', _text_pdf.upper())
        if (len(_valor_nota) > 0):
            _dict_data.update({'valor': _valor_nota[0].strip()})

        ## captura nome do emissor
        _nomes = re.findall(r'(?<=RAZÃO\sSOCIAL:\s)(.*)', _text_pdf.upper())
        for _nome in _nomes:
            if ('' not in _nome):
                ## capturar somente dígitos
                _nome = re.sub('[0-9]', '', _nome).strip()
                _dict_data.update({'nome': _nome})
                break

        ## captura mês vigente
        _mes_vigente = re.findall(r'(?<=FINANÇAS\s)(.*)', _text_pdf.upper())
        if (len(_mes_vigente) > 0):
            _dict_data.update({'mes_vigente': _mes_vigente[0][3:10]})
    else:
        _dict_data.update({'valor': 'informacao nao encontrada'})
        _dict_data.update({'nome': 'informacao nao encontrada'})
        _dict_data.update({'mes_vigente': 'informacao nao encontrada'})
        ## mandar email para nós quando acontecer isso