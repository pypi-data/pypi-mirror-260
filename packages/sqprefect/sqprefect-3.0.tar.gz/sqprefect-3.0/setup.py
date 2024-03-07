from setuptools import setup, find_packages
try:
    from sqprefect.package._package import __name__, __version__
except:
    __name__ = 'sqprefect'
    __version__ = '2.4.38'

setup(
    name=__name__,
    version='3.0',
    packages=find_packages(),
    description=__name__,
    author='Bill Johnson',
    author_email='bjohnson@squareup.com',
    install_requires=[
    ],
)
