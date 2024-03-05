from setuptools import setup, find_packages

setup(
    name='mymark',
    version='1.0.3',
    packages=find_packages(),
    scripts=['src/marker/mymark/mymark.py'],
    install_requires=[
        'aiohttp',
        'pytest',
        'pylint',
        'mypy',
    ]
)
