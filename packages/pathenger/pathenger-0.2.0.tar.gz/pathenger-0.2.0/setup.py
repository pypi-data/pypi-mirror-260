from setuptools import setup, find_packages

setup(
    name="pathenger",
    version="0.2.0",
    author="p12m3ikm4d",
    author_email="issue.no9@gmail.com",
    description='A utility package for determining the paths of executable files and temporary directories, especially useful for applications packaged with PyInstaller.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/p12m3ikm4d/pathenger",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)