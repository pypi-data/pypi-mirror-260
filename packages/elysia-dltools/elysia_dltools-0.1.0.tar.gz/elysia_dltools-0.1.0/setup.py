from setuptools import setup
from setuptools import find_packages


VERSION = '0.1.0'

setup(
    name='elysia_dltools',  # 包名
    version=VERSION,        # 版本
    description='Elysia DeepLearning Tools', # 包简介
    packages=find_packages(),
    zip_safe=False,
    author='ElysiaAILab'            ,# 作者
    author_email='3518925535@qq.com',# 作者邮件
)

'''
setup(
    name='',#包名
    version='',#版本
    description="",#包简介
    long_description=open('README.md').read(),# 读取文件中介绍包的详细内容
    include_package_data=True,# 是否允许上传资源文件
    author='',#作者
    author_email='',#作者邮件
    maintainer='',#维护者
    maintainer_email='',#维护者邮件
    license='MIT License',#协议
    url='',#github或者自己的网站地址
    packages=find_packages(),#包的目录
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
     'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',#设置编写时的python版本
],
    python_requires='>=3.9',#设置python版本要求
    install_requires=[''],#安装所需要的库
    entry_points={
        'console_scripts': [
            ''],
    },#设置命令行工具(可不使用就可以注释掉)
    
)
这就是一些常用的，其他的不需要根本不用填
————————————————

                            版权声明：本文为博主原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接和本声明。
                        
原文链接：https://blog.csdn.net/qq_53280175/article/details/121509970

'''