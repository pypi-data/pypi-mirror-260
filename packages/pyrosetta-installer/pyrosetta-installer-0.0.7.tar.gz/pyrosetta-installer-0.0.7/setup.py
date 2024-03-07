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

To install PyRosetta, after installing package, run:

```python -c 'import pyrosetta_installer; pyrosetta_installer.install_pyrosetta()'```

It is also possible to supply optional `serialization=True` argument in case PyRosetta build with serialization and thread support is needed.

'''

setup(
    name='pyrosetta-installer',
    version='0.0.7',
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
