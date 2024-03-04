import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="example_python_package_ulturgashev",
    version="0.0.1",
    author="ulturgashev",
    author_email="ulturgashevvv@gmail.com",
    description="Example python package",
    long_description=long_description,
    url="https://github.com/ulturgashev/example_python_package",
    packages=setuptools.find_packages()
)
