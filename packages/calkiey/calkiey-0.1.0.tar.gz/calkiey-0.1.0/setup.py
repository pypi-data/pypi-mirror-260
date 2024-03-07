from setuptools import setup, find_packages

setup(
    name='calkiey',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
       'tk',
       'pillow',
       'numpy',
    ],
    entry_points={
        'console_scripts': [
            'calkiey=calkiey:main',
        ],
    },
)
