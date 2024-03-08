# ISeqDb_PyPI/setup.py
# Nico Salmaso - nico.salmaso@fmach.it

from setuptools import setup, find_packages

setup(
    name='ISeqDb',
    version='0.0.2',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ISeqDb = ISeqDb.ISeqDb:main'
        ]
    },
    include_package_data=True,
    install_requires=['pandas'],
)
