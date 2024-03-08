#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nanh_easy_google_search',
    version='1.0.0',
    author='nanh',
    author_email='877007021@qq.com',
    url='https://github.com/877007021/easy_google_search',
    description='Google搜索工具',
    long_description=long_description,
    long_description_content_type='text/markdown',  # 指定描述内容类型为 Markdown 格式
    packages=['nanh_easy_google_search'],
    install_requires=["beautifulsoup4", "Requests", "urllib3"],
)
