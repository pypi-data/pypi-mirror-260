#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    "PyYAML",
    "Rich",
    "pandas",
    "xlsxwriter"
]

test_requirements = [ ]

setup(
    author="Jaideep Sundaram",
    author_email='jai.python3@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Collection of Python scripts/utils for file manipulation tasks",
    entry_points={
        'console_scripts': [
            'csv2tsv=data_file_utils.csv2tsv:main',
            'tsv2json=data_file_utils.tsv2json:main',
            'analyze-record-tuples=data_file_utils.analyze_record_tuples:main',
            'compare-tab-files=data_file_utils.compare_tab_files:main',
            'jsonl2json=data_file_utils.jsonl2json:main',
            'xlsx2tsv=data_file_utils.xlsx2tsv:main',
            'delete-old-files=data_file_utils.delete_users_files:main',
            'backup-file=data_file_utils.backup_file:main',
            'archive-dir=data_file_utils.archive_dir:main',
            'backup-dir=data_file_utils.backup_dir:main',
            'create-tmp-dir=data_file_utils.create_tmp_dir:main',
            'profile-data-file=data_file_utils.profile_data_file:main',
            'find-last-file=data_file_utils.find_last_file:main',
            'find-last-directory=data_file_utils.find_last_directory:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='data_file_utils',
    name='data_file_utils',
    packages=find_packages(include=['data_file_utils', 'data_file_utils.*']),
    package_data={"data_file_utils": ["conf/config.yaml"]},
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jai-python3/data-file-utils',
    version='0.9.0',
    zip_safe=False,
)
