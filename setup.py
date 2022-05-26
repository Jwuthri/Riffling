from setuptools import setup, find_packages

version = "1.0.0"

setup(
    name="bionic-reading",
    version=version,
    license="proprietary",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
