from setuptools import setup, find_packages

setup(
    name="aoe2netapi",
    version="0.1.0",
    description="A simple and basic API wrapper for the https://aoe2.net/#api.",
    url="ENTER_GITHUB_LINK_HERE",
    license="MIT",
    author="sixP-NaraKa",
    author_email="ADD EMAIL HERE",
    packages=find_packages(),
    install_requires=[
        "requests>=2.20.0"
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python 3",
    ]
)
