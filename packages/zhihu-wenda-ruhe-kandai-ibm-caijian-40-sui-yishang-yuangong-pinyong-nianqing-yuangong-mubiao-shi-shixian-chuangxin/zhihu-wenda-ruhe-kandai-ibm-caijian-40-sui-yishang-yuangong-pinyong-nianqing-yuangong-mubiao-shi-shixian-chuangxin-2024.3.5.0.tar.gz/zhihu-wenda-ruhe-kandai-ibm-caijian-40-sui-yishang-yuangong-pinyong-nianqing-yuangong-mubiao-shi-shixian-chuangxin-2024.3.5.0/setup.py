#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import ZhihuWendaRuheKandaiIbmCaijian40SuiYishangYuangongPinyongNianqingYuangongMubiaoShiShixianChuangxin
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('ZhihuWendaRuheKandaiIbmCaijian40SuiYishangYuangongPinyongNianqingYuangongMubiaoShiShixianChuangxin'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="zhihu-wenda-ruhe-kandai-ibm-caijian-40-sui-yishang-yuangong-pinyong-nianqing-yuangong-mubiao-shi-shixian-chuangxin",
    version=ZhihuWendaRuheKandaiIbmCaijian40SuiYishangYuangongPinyongNianqingYuangongMubiaoShiShixianChuangxin.__version__,
    url="https://github.com/apachecn/zhihu-wenda-ruhe-kandai-ibm-caijian-40-sui-yishang-yuangong-pinyong-nianqing-yuangong-mubiao-shi-shixian-chuangxin",
    author=ZhihuWendaRuheKandaiIbmCaijian40SuiYishangYuangongPinyongNianqingYuangongMubiaoShiShixianChuangxin.__author__,
    author_email=ZhihuWendaRuheKandaiIbmCaijian40SuiYishangYuangongPinyongNianqingYuangongMubiaoShiShixianChuangxin.__email__,
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
    description="知乎问答：如何看待 IBM 裁减 40 岁以上员工，聘用年轻员工，目标是实现创新？",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "zhihu-wenda-ruhe-kandai-ibm-caijian-40-sui-yishang-yuangong-pinyong-nianqing-yuangong-mubiao-shi-shixian-chuangxin=ZhihuWendaRuheKandaiIbmCaijian40SuiYishangYuangongPinyongNianqingYuangongMubiaoShiShixianChuangxin.__main__:main",
            "ZhihuWendaRuheKandaiIbmCaijian40SuiYishangYuangongPinyongNianqingYuangongMubiaoShiShixianChuangxin=ZhihuWendaRuheKandaiIbmCaijian40SuiYishangYuangongPinyongNianqingYuangongMubiaoShiShixianChuangxin.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
