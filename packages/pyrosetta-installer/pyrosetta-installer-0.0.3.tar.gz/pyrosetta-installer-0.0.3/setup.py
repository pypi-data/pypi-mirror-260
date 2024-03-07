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
    version='0.0.3',
    description='Download PyRosetta wheel package from PyRosetta.org and install it',
    long_description='Download PyRosetta wheel package from one of PyRosetta.org mirrors and install it.\nNote that USE OF PyRosetta FOR COMMERCIAL PURPOSES REQUIRE PURCHASE OF A LICENSE.\nSee https://github.com/RosettaCommons/rosetta/blob/main/LICENSE.md or email license@uw.edu for details.',
    url='https://www.pyrosetta.org/',
    author='Sergey Lyskov',
    author_email='sergey.lyskov@jhu.edu',
    license='Rosetta Software License',
    packages=['pyrosetta_installer'],
    zip_safe=False,
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
