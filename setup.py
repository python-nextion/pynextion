from setuptools import setup, find_packages
from os import path
import io


here = path.abspath(path.dirname(__file__))


NAME = 'pynextion'
with io.open(path.join(here, NAME, 'version.py'), 'rt', encoding='UTF-8') as f:
    exec(f.read())


with io.open(path.join(here, 'README.md'), 'rt', encoding='UTF-8') as f:
    long_description = f.read()


setup(
    name=NAME,
    version="0.0.1",
    author="Raffaele Montella",
    author_email="raffaele.montella@uniparthenope.it",
    description="Python library for Nextion intelligent display",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=__license__,
    keywords="nextion display screen library",
    url=__url__,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache 2.0 License",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
