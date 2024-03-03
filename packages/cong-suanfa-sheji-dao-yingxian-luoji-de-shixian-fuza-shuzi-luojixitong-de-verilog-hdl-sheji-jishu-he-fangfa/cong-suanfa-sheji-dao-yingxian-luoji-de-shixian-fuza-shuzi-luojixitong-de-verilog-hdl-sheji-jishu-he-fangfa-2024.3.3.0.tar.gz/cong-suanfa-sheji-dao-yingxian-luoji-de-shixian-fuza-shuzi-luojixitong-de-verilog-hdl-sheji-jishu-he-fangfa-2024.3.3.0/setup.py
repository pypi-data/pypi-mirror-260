#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import CongSuanfaShejiDaoYingxianLuojiDeShixianFuzaShuziLuojixitongDeVerilogHdlShejiJishuHeFangfa
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('CongSuanfaShejiDaoYingxianLuojiDeShixianFuzaShuziLuojixitongDeVerilogHdlShejiJishuHeFangfa'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="cong-suanfa-sheji-dao-yingxian-luoji-de-shixian-fuza-shuzi-luojixitong-de-verilog-hdl-sheji-jishu-he-fangfa",
    version=CongSuanfaShejiDaoYingxianLuojiDeShixianFuzaShuziLuojixitongDeVerilogHdlShejiJishuHeFangfa.__version__,
    url="https://github.com/apachecn/cong-suanfa-sheji-dao-yingxian-luoji-de-shixian-fuza-shuzi-luojixitong-de-verilog-hdl-sheji-jishu-he-fangfa",
    author=CongSuanfaShejiDaoYingxianLuojiDeShixianFuzaShuziLuojixitongDeVerilogHdlShejiJishuHeFangfa.__author__,
    author_email=CongSuanfaShejiDaoYingxianLuojiDeShixianFuzaShuziLuojixitongDeVerilogHdlShejiJishuHeFangfa.__email__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: Other/Proprietary License",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Documentation",
        "Topic :: Documentation",
    ],
    description="从算法设计到硬线逻辑的实现--复杂数字逻辑系统的 Verilog HDL 设计技术和方法",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "cong-suanfa-sheji-dao-yingxian-luoji-de-shixian-fuza-shuzi-luojixitong-de-verilog-hdl-sheji-jishu-he-fangfa=CongSuanfaShejiDaoYingxianLuojiDeShixianFuzaShuziLuojixitongDeVerilogHdlShejiJishuHeFangfa.__main__:main",
            "CongSuanfaShejiDaoYingxianLuojiDeShixianFuzaShuziLuojixitongDeVerilogHdlShejiJishuHeFangfa=CongSuanfaShejiDaoYingxianLuojiDeShixianFuzaShuziLuojixitongDeVerilogHdlShejiJishuHeFangfa.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
