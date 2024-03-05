from setuptools import find_packages, setup
setup(
    name='imagify',
    packages=find_packages(include=['imagify']),
    version='1.0.6',
    description='Revolutionize your text into stunning visual art with our Python library! Convert plain text into captivating images effortlessly',
    author='Muhammad Asif Ali',
    include_package_data=True,
    package_data={'': ['config.toml']},
    install_requires=['selenium','toml','requests']
)

