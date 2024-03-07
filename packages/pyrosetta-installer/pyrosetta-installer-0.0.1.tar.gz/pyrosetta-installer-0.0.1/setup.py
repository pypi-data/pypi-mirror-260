from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

from pyrosetta_installer import *

class PostDevelopCommand(develop):
    def run(self):
        develop.run(self)
        #install_pyrosetta()


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        #install_pyrosetta()


setup(
    name='pyrosetta-installer',
    version='0.0.1',
    description='Download PyRosetta wheel package from PyRosetta.org and install it',
    url='https://github.com/RosettaCommons/pyrosetta-installer',
    author='Sergey Lyskov',
    author_email='sergey.lyskov@jhu.edu',
    license='MIT',
    packages=['pyrosetta_installer'],
    zip_safe=False,
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
