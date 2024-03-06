
from setuptools import setup, find_packages
try:
    from sq_protos_py.package._package import __name__, __version__
except:
    __name__ = 'sq_protos_py'
    __version__ = '20240322.265933'

setup(
    name=__name__,
    version=__version__,
    packages=find_packages(),
    description=__name__,
    author='James Williams',
    author_email='jwilliams@square.ic',
    install_requires=[
    ],
)
