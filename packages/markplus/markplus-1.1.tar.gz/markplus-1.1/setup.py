from setuptools import find_packages, setup

setup(
    name="markplus",
    version="1.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "markplus=marker_tool.mymark:main",
        ],
    },
    install_requires=[
        "requests==2.31.0",
    ],
)
