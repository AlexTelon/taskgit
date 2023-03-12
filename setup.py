from setuptools import setup, find_packages

setup(
    name='taskgit',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'taskgit=taskgit.generator:main',
        ],
    },
    install_requires=[
        'toml',
    ],
)
