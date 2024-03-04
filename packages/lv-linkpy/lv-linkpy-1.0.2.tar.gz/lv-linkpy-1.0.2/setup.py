import setuptools
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding="utf-8") as f:
    description = f.read()

setuptools.setup(
    name="lv-linkpy",
    version="1.0.2",
    description="a python interface to remote LabVIEW controls",
    author="ZHUO DIAO",
    author_email="enzian0515@gmail.com",
    license="MIT",
    packages=setuptools.find_packages(),
    long_description=description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=["numpy"],
    python_requires='>=3.6',
)