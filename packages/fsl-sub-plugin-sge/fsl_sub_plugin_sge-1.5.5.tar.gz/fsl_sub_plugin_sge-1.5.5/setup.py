#!/usr/bin/env python
from setuptools import setup, find_packages

with open('fsl_sub_plugin_sge/version.py', mode='r') as vf:
    vl = vf.read().strip()

PLUGIN_VERSION = vl.split(' = ')[1].strip("'")

with open('README.md', mode='rt') as f:
    README = f.read().strip()

setup(
    name='fsl_sub_plugin_sge',
    version=PLUGIN_VERSION,
    description='FSL Cluster Submission Plugin for Son of/Univa Grid Engine',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Duncan Mortimer',
    author_email='duncan.mortimer@ndcn.ox.ac.uk',
    url='https://git.fmrib.ox.ac.uk/fsl/fsl_sub_plugin_sge',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Natural Language :: English',
        'Environment :: Console',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
    ],
    keywords='FSL fsl Neuroimaging neuroimaging cluster'
             ' grid slurm grid engine',
    project_urls={
        'Documentation': 'https://fsl.fmrib.ox.ac.uk/fsl/fslwiki',
        'Source': 'https://git.fmrib.ox.ac.uk/fsl/fsl_sub_plugin_sge'
    },
    packages=find_packages(),
    license='Apache License Version 2.0',
    install_requires=['fsl_sub>=2.7.0', 'ruamel.yaml>=0.16.7', ],
    python_requires='~=3.7',
    package_data={
        'fsl_sub_plugin_sge': ['fsl_sub_sge.yml', 'README.md', 'CHANGES.md', 'INSTALL.md', 'BUILD.md'],
    },
    include_package_data=True,
)
