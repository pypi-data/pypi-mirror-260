
from setuptools import setup, find_packages

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setup(
    name="py_eth_utils",
    version="0.0.2",
    packages=find_packages(),
    # 依赖库
    install_requires=[
        'web3==6.15.1'
    ],
    author="Stars Bing",
    author_email="bing@starsxu.com",
    description="eth for tools, contracts、transfer、balance",
    long_description="",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License"
    ]
)