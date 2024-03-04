from setuptools import setup, find_packages
import pkg_resources, pathlib

with pathlib.Path("requirements.txt").open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name="molecular_structure",
    version="0.0.1",
    packages=find_packages(),
    description="Computing Molecular structure with Python",
    install_requires=install_requires,
)
