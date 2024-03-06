from setuptools import setup, find_packages

VERSION = '0.0.8'
DESCRIPTION = 'Robot Luca api package'

setup(
    name="luca_api",
    version=VERSION,
    author="HorusAI",
    author_email="quyennt@horusvn.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows/ Ubuntu",
    ],
)



