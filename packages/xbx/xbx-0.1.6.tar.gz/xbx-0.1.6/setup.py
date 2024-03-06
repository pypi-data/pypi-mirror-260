from setuptools import setup

package_data = {
    'xtquant': ['xtquant/*'],# ['xtquant/*']代表移动文件的路径，如果有其他类似情况按这个格式往下加就行
}

setup(
    name='xbx',
    version='0.1.6',# 版本号
    description='xbx',
    author='xbx',
    packages=['xtquant'], # package_data的key
    package_data=package_data, # 不用改了
    include_package_data=True,
    install_requires=[  # 用到的库，有需要的往下加
        'ccxt==2.2.40',
        'dataframe_image==0.1.5',
        'DrissionPage==3.2.34',
        'lxml==4.8.0',
        'ntplib==0.4.0',
        'httpx==0.26.0',
        'bs4==0.0.2',
        'tabulate==0.8.9',
        'py-mini-racer==0.6.0',
        'psutil==5.9.6',
        'matplotlib==3.7.2',
        'joblib==1.3.2',
        'numpy==1.22.4',
        'pandas==1.5.3',
        'requests==2.31.0',
        'tqdm==4.66.1',
        'plotly==5.6.0',
        'pyarrow==14.0.0',
        'retrying==1.3.3',
        'scipy==1.7.3',
        'scikit-learn==1.3.0',
    ],
)
