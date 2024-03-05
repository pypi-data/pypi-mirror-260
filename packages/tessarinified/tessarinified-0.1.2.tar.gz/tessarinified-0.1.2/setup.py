from setuptools import find_packages, setup
import os

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


version = '0.1.2'

test = False

setup(
    name='tessarinified',
    packages=find_packages(include=['tessarinified']),
    version=version,
    description='n-complex numbers (Tessarines) in Python',
    author='corruptconverter, slycedf, goblinovermind, jerridium',
    install_requires=['numpy'],
    license='MIT',
    long_description=read('README.md'),
    classifiers=["Development Status :: 3 - Alpha"]
)

token = open(f'D:/slycefolder/ins/tsr/{ {True: "tt", False: "tr"}[test] }', 'r').read()

os.system(f'twine upload --repository { {True: "testpypi", False: "pypi"}[test] } dist/*{version}* -u __token__ -p {token} --verbose')
