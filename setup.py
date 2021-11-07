from setuptools import setup, find_packages

readme = ""
with open("README.md") as f:
    readme = f.read()

setup(
    name="aoe2netapi-wrapper",
    version="1.1.1",
    description="A simple and basic Python 3 API wrapper for the https://aoe2.net/#api API.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/sixP-NaraKa/aoe2net-api-wrapper",
    license="MIT",
    author="sixP-NaraKa",
    author_email="sixpaths-naraka@protonmail.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.20.0"
    ],
    python_requires=">=3.5",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ]
)
