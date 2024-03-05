import os
from setuptools import setup
from setuptools.command.install import install

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

class CustomInstallCommand(install):
    """Customized setuptools install command - prints a friendly greeting."""
    def run(self):
        print("Installing dvc_objects_hdfs38 as dvc_objects (hdfs dvc pull bugfix github.com/iterative/dvc/issues/8642)")
        install.run(self)
        

setup(
    name = "dvc_objects_hdfs38",
    version = "3.0.7",
    author = "Ivan Tyurin",
    author_email = "3464mustang+test_pypi@gmail.com",
    description = "original dvc-objects_3.0.6 with hdfs support tqdm (github.com/iterative/dvc/issues/8642) - filesystem and object-db level abstractions to use in dvc and dvc-data",
    license = "Apache-2.0",
#    url = "http://packages.python.org/dvc_objects_3.0.6",
    packages=["dvc_objects"],
    long_description=read("README.rst"),
    install_requires=[
        'fsspec',
        'funcy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    project_urls = {
        'Issues': 'https://github.com/TyurinIvan/dvc-objects/issues',
        'Source': 'https://github.com/TyurinIvan/dvc-objects'
    },
    cmdclass={
        'install': CustomInstallCommand,
    },
)

