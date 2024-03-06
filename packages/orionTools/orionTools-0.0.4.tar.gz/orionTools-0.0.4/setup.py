from setuptools import setup, find_packages

setup(
    name="orionTools",
    version="0.0.4",
    keywords=["orion", "orionTools"],
    description="orion tools",
    long_description="orion 专用的 tools 工具库。",
    license="MIT",

    url="https://github.com/eqauto/orion-tools.git",
    author="eqauto",
    author_email="eqauto@yeah.net",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[]
)

"""
项目打包
python setup.py bdist_egg           # 生成类似 eqlink-0.0.1-py2.7.egg，支持 easy_install 
# 使用此方式
python setup.py sdist bdist_wheel   # 生成类似 eqlink-0.0.1.tar.gz，支持 pip
# twine 需要安装（pip install twine）
twine upload dist/*
"""
