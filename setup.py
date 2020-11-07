from setuptools import setup, find_packages

readme = ""
with open("README.md") as f:
    readme = f.read()

setup(
    name="aoe2netapi-wrapper",
    version="0.1.0",
    description="A simple and basic Python wrapper for the https://aoe2.net/#api API.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="ENTER_GITHUB_LINK_HERE",
    license="MIT",
    author="sixP-NaraKa",
    author_email="sixpaths-naraka@protonmail.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.20.0"
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ]
)
