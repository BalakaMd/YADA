import setuptools

setuptools.setup(
    name="yada",
    version="0.1.0",
    author="YADA Team",
    description="This is a yada package.",
    url="https://github.com/BalakaMd/YADA",
    packages=['yada'],
    install_requires=[
        'prompt-toolkit==3.0.43',
        'tabulate==0.9.0',
        'wcwidth==0.2.12',
    ],
    entry_points={
        'console_scripts': [
            'yada = yada.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)