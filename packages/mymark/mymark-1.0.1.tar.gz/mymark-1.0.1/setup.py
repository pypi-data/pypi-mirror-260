from setuptools import setup, find_packages

setup(
    name='mymark',
    version='1.0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mymark=mymark:main',
        ],
    },
    install_requires=[
        'aiohttp',
        'pytest',
        'pylint',
        'mypy',
    ]
)
