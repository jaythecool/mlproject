from setuptools import find_packages,setup
from typing import List

def get_requirements(file_path:str)->List[str]:

    requirements = []

    with open(file_path) as file:
        requirements = file.readlines()
        requirements = [requirement.replace("\n","") for requirement in requirements ]

        if "-e ." in requirements:
            requirements.remove("-e .")
    return requirements

setup(
    name="mlproject",
    version="0.0.1",
    author="Jayesh",
    author_email="jayeshvengurlekar7@gmail.com",
    packages=find_packages(),
    requires=get_requirements("requirements.txt")
)

