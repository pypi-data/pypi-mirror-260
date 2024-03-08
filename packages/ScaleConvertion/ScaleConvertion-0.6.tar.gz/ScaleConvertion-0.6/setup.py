# -*- coding: utf-8 -*-
# @Time    : 2023/4/9 21:34
# @Author  : qxcnwu
# @FileName: setup.py
# @Software: PyCharm
from setuptools import setup, find_packages

setup(
    name='ScaleConvertion',  # 包名
    version='0.6',  # 版本
    description="Helps achieve surface reflectance scale conversion",  # 包简介
    long_description=open('README.rst').read(),  # 读取文件中介绍包的详细内容
    include_package_data=True,  # 是否允许上传资源文件
    author='qxcnwu',  # 作者
    author_email='qxcnwu@gmail.com',  # 作者邮件
    maintainer='qxcnwu',  # 维护者
    maintainer_email='qxcnwu@gmail.com',  # 维护者邮件
    license='MIT License',  # 协议
    url='https://github.com/qxcnwu',  # github或者自己的网站地址
    packages=find_packages(),  # 包的目录
    package_data={"": ["*.pth"]},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',  # 设置编写时的python版本
    ],
    python_requires='>=3.4',  # 设置python版本要求
    install_requires=['tqdm', 'numpy', 'pandas', 'torch', 'timm', 'exifread', 'qt5_applications', 'matplotlib',
                      'torchvision', 'requests', 'colour', 'opencv-python','gdal'],  # 安装所需要的库
    # entry_points={
    #     'console_scripts': [
    #         ''],
    # },  # 设置命令行工具(可不使用就可以注释掉)

)
