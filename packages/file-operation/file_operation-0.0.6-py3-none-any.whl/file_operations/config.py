# -*- coding: utf-8 -*-
"""
@Time : 2024/3/6 11:56 
@项目：文件使用
@File : config.by
@PRODUCT_NAME :PyCharm
"""
import os

DIRNAME = os.path.dirname(os.path.abspath(__file__))
PANDOCPATH = os.path.join(DIRNAME, "media", "Pandoc", 'pandoc.exe')
WKHTMLTOXPATH = os.path.join(DIRNAME, "media", "wkhtmltox", 'wkhtmltopdf.exe')
