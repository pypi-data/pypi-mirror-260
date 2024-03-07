from setuptools import setup, find_packages

setup(
    name='Tflask',  # 包的名称
    version='1.0.0',          # 包的版本号
    author='Dingyao Li',       # 作者名字
    author_email='675391321@qq.com',  # 作者邮箱
    description='Trading backtesting',  # 包的简要描述
    long_description=open('README.md').read(),  # 包的详细描述，通常从 README 文件中读取
    long_description_content_type='text/markdown',  # 描述内容的类型
    url='https://github.com/DingyaoLi2024/Tflask----incompleted-version',  # 你的包的代码存储库 URL
    packages=find_packages(),  # 寻找所有的 Python 包
    classifiers=[  # 包的分类信息
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',  # 特定的 Python 版本
        'Operating System :: POSIX :: Linux',  # 仅适用于 Linux 系统
    ],
    python_requires='>=3.8',  # 指定所需的 Python 版本
)
