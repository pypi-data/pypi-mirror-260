from setuptools import find_packages, setup

setup(
    name="mymarkv2",
    version="1.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "mymark=marker_tool.mymark:main",
        ],
    },
    install_requires=[
        "requests==2.31.0",
    ],
)
