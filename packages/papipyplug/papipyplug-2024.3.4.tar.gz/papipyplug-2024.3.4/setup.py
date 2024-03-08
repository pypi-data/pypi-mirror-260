from setuptools import setup, find_packages
from datetime import datetime

version_timestamp = datetime.now().strftime("%Y.%m")
version_patch = 4
version = f"{version_timestamp}.{version_patch}"


setup(
    name="papipyplug",
    version=version,
    author="Seth Lawler",
    description="Utilities to facilitate the conversion of python programs to plugins for use in the dewberry/process-api",
    license="MIT",
    packages=find_packages(),
    install_requires=[],
)
