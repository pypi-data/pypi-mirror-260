from setuptools import setup, find_packages

setup(
    name="silog",
    version="0.1.3",
    author="p12m3ikm4d",
    author_email="issue.no9@gmail.com",
    description="A simple logging library",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/p12m3ikm4d/silog",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)