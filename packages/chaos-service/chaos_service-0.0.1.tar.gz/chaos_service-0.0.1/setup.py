import setuptools
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
long_description = ""
with open("README.md", "r") as fh:
    long_description = fh.read()

with open(os.path.join(__location__, 'requirements.txt')) as f:
    required = f.read().splitlines()


setuptools.setup(name="chaos_service",version="0.0.1",
                 author="Hevo Technology Team",description="Service to inject a chaos in Hevo 2.0 services",
                 packages=setuptools.find_packages(), include_package_data=True,author_email="",url="",
                 install_requires=required, long_description=long_description,
                 python_requires='>=3.9'
)