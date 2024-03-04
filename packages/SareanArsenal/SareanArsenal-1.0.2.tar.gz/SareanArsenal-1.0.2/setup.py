from setuptools import setup, find_packages

setup(
    name='SareanArsenal',
    version='1.0.2',
    author='FF14.CN ORG.',
    author_email='hi@ff14.cn',
    description='A FF14CN Tool kit',
    packages=find_packages(),
    install_requires=['requests',
                      'kuai_log',
                      'pyzbar',
                      'pillow',],
)