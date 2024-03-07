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

long_description = '''\
Download PyRosetta wheel package from one of www.PyRosetta.org mirrors and install it.

**Note that USE OF PyRosetta FOR COMMERCIAL PURPOSES REQUIRE PURCHASE OF A LICENSE.**

See https://github.com/RosettaCommons/rosetta/blob/main/LICENSE.md or email license@uw.edu for details.
'''

setup(
    name='pyrosetta-installer',
    version='0.0.5',
    description='Download PyRosetta wheel package from PyRosetta.org and install it',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://www.pyrosetta.org/',
    author='Sergey Lyskov',
    license='Rosetta Software License',
    packages=['pyrosetta_installer'],
    zip_safe=False,
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
