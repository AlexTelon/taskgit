from setuptools import setup, find_packages

setup(
    name="taskgit",
    version="0.1",
    packages=find_packages(),
    package_data={
        "taskgit": ["style.css"],
    },
    entry_points={
        "console_scripts": [
            "taskgit=taskgit.main:main",
        ],
    },
    install_requires=[
        "toml",
    ],
)
