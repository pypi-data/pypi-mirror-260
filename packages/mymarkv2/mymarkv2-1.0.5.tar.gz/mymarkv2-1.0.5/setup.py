from setuptools import find_packages, setup

setup(
    name="mymarkv2",
    version="1.0.5",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "mymark=mymark.mymark:main",
        ],
    },
    install_requires=[
        "requests==2.31.0",
    ],
)
