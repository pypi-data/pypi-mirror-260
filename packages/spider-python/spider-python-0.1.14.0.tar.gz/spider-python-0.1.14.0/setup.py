from setuptools import setup, find_packages
from Cython.Build import cythonize

setup(
    name="spider-python",
    version="0.1.14.0",
    packages=find_packages(),
    install_requires=[
        "Cython",# 在这里列出你的库所需的其他Python包
        "numpy",
        "scipy",
        "matplotlib",
    ],
    # install_requires 在安装模块时会自动安装依赖包
    # 而 extras_require 不会，这里仅表示该模块会依赖这些包
    # 但是这些包通常不会使用到，只有当你深度使用模块时，才会用到，这里需要你手动安装
    extras_require={
        'opencv-python': ["opencv-python"],
    },

    ext_modules=cythonize("spider/elements/*.pyx"), # 现在感觉好像不起效

    author="Zelin Qian",
    author_email="qzl22@mails.tsinghua.edu.cn",

    description="SPIDER -- Self-driving Planning and Intelligent Decision-making Engine with Reinforcement learning",
    long_description=open("README.md",encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/ZelinQian/SPIDER",
    # classifiers=[
    #     "Development Status :: 3 - Alpha",
    #     "Intended Audience :: Developers",
    #     "License :: OSI Approved :: MIT License",
    #     "Programming Language :: Python",
    #     "Programming Language :: Python :: 3",
    #     "Programming Language :: Python :: 3.6",
    #     "Programming Language :: Python :: 3.7",
    #     "Programming Language :: Python :: 3.8",
    #     "Programming Language :: Python :: 3.9",
    # ],
)
