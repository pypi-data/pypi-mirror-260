from setuptools import setup



from setuptools import setup, find_packages

setup(
    name='Taowa',
    version='1.0.0',
    description='常用基础命令',
    long_description_content_type='text/markdown',
    author='',
    author_email='',
    packages=find_packages(),

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    # 如果有依赖包，可以在此处添加
    install_requires=[
        'requests',
        'PyExecjs',
    ],
)