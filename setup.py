from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="taskgit",
    version="0.1",
    packages=find_packages(),
    package_data={
        "taskgit": ["style.css", "script.js"],
    },
    entry_points={
        "console_scripts": [
            "taskgit=taskgit.main:main",
        ],
    },
    install_requires=requirements,
)
