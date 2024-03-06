from setuptools import setup, find_packages

setup(
    name='enigma_tpenha_junq',
    version='0.1',
    description='Enigma solving machine using numpy',
    packages=find_packages(),
    author = 'Thiago Penha',
    author_email = 'tpenha30@gmail.com',
    install_requires=[
        'numpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    )