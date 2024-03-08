from setuptools import setup



from setuptools import setup, find_packages

setup(
    name='Taowa_skin',
    version='1.0.0',
    description='Skin皮肤模块',
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
)