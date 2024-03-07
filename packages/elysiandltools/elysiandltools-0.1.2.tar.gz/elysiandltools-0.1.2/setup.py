from setuptools import setup
from setuptools import find_packages


VERSION = '0.1.2'

setup(
    name='elysiandltools',  # 包名
    version=VERSION,        # 版本
    description='Elysia DeepLearning Tools', # 包简介
    packages=find_packages(),
    zip_safe=False,
    author='ElysiaAILab'            ,# 作者
    author_email='3518925535@qq.com',# 作者邮件
)


'''
python setup.py sdist build
twine upload dist/*
pip install elysiandltools==0.1.1 -i https://pypi.org/simple 
'''