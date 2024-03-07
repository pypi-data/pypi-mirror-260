from setuptools import setup, find_packages
try:
    from sq_metrics.package._package import __name__, __version__
except:
    __name__ = 'sq-metrics'
    __version__ = '0.9.1'

setup(
    name=__name__,
    version=__version__,
    packages=find_packages(),
    description=__name__,
    author='Cindy Jones',
    author_email='cjones@squareup.com',
    install_requires=[
    ],
)
