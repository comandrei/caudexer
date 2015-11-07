import setuptools
import os


def requirements(path="dexer/requirements.txt"):
    here = os.path.dirname(os.path.realpath(__file__))
    full_path =  os.path.join(here, path)
    with open(full_path, 'r') as fp:
        return fp.readlines()


setuptools.setup(
    name='caudexer',
    version='0.1.0',
    install_requires=requirements(),
    packages=['dexer/dexer', 'dexer/caudexer'],
)
