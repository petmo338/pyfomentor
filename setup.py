from setuptools import setup, find_packages

setup(
    name="pyfomentor",
    version="0.1.0",
    url="https://github.com/petmo338/pyformentor.git",
    author="Peter Möller",
    author_email="petmo338@gmail.com",
    description="grab infomentor data and and return as json",
    packages=find_packages(),
    entry_points = {
        'console_scripts': [
            'pyfomentor=pyfomentor.main:main'
        ],
    },
    install_requires=['requests']
)
