#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import ZhihuWendaRuheKandaiBuJieshou996JiushiChiBuleKuDeLundiao
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('ZhihuWendaRuheKandaiBuJieshou996JiushiChiBuleKuDeLundiao'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="zhihu-wenda-ruhe-kandai-bu-jieshou-996-jiushi-chi-bule-ku-de-lundiao",
    version=ZhihuWendaRuheKandaiBuJieshou996JiushiChiBuleKuDeLundiao.__version__,
    url="https://github.com/apachecn/zhihu-wenda-ruhe-kandai-bu-jieshou-996-jiushi-chi-bule-ku-de-lundiao",
    author=ZhihuWendaRuheKandaiBuJieshou996JiushiChiBuleKuDeLundiao.__author__,
    author_email=ZhihuWendaRuheKandaiBuJieshou996JiushiChiBuleKuDeLundiao.__email__,
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
    description="知乎问答：如何看待「不接受 996 就是吃不了苦」的论调？",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "zhihu-wenda-ruhe-kandai-bu-jieshou-996-jiushi-chi-bule-ku-de-lundiao=ZhihuWendaRuheKandaiBuJieshou996JiushiChiBuleKuDeLundiao.__main__:main",
            "ZhihuWendaRuheKandaiBuJieshou996JiushiChiBuleKuDeLundiao=ZhihuWendaRuheKandaiBuJieshou996JiushiChiBuleKuDeLundiao.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
