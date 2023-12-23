from setuptools import setup, find_packages

setup(
    name='yada',
    version='0.1.0',
    packages=find_packages(where='src'),
    install_requires=[
        'prompt-toolkit==3.0.43',
        'tabulate==0.9.0',
        'wcwidth==0.2.12',
    ],
    entry_points={
        'console_scripts': [
            'yada = src.main:main',
        ],
    },
)
