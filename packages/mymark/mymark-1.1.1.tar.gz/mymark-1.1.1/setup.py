from setuptools import setup

setup(
    name='mymark',
    version='1.1.1',
    packages=['/Users/shwetabanerjee/Desktop/University/Imperial/Year3Modules/SWE/segp-17/marker/mymark'],
    entry_points={
        'console_scripts': [
            'mymark = src.marker.mymark.mymark:main',
        ],
    },
    install_requires=[
        'aiohttp',
        'pytest',
        'pylint',
        'mypy',
    ],
)
