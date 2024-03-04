# -*- coding: utf-8 -*-
# @Time    : 2024/3/4 10:38
# @Author  : Chen_Shi_Chao
# @Email   : M202373504@hust.edu.cn
# @File    : setup.py
# @Software: PyCharm
from setuptools import setup

setup(
    name='MyModel_CSC',# 需要打包的名字,即本模块要发布的名字
    version='v1.0',#版本
    description='A  module for test', # 简要描述
    py_modules=['MyModel_CSC'],   #  需要打包的模块
    author='CSC_HUST', # 作者名
    author_email='zzucsc@163.com',   # 作者邮件
    url='https://github.com/hustcsc?tab=projects', # 项目地址,一般是代码托管的网站
    requires=['numpy'], # 依赖包,如果没有,可以不要
    license='MIT'
)