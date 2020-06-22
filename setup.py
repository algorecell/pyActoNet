
from setuptools import setup, find_packages

setup(name="actonet",
    version="9999",
    description = "Abduction-based control of Boolean networks fixpoints",
    install_requires = [
        "algorecell_types",
        "asprin",
        "colomoto_jupyter",
    ],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    keywords="computational systems biology",

    include_package_data = True,
    packages = find_packages()
)

