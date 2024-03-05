from setuptools import setup, find_packages
import os

VERSION = "0.0.0"
DESCRIPTION = "Fintekkers DevOps package"
LONG_DESCRIPTION = "Contains DevOps scripts to deploy services to public cloud"

if "BUILD_VERSION" in os.environ:
    print("******************************************")
    print("************OVERRIDING VERSION FROM ENVIRONMENT******************")
    print("******************************************")
    VERSION = os.environ.get("BUILD_VERSION")

setup(
    name="fintekkers-devops-scripts",
    license="MIT",
    author="David Doherty",
    author_email="dave@fintekkers.org",
    include_package_data=True,
    url="https://github.com/fintekkers/fintekkers-devops-scripts",
    keywords="fintekkers ledger models",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
    ],
)
