from setuptools import setup, find_packages

setup(
    author_email="arun.kumar@swimming.org.au",
    author="Arun Kumar",
    classifiers=[
        "Topic :: Software Development :: Build Tools",
    ],
    description="Calculation for Sparta",
    install_requires=["glom"],
    license="MIT",
    name="spartaCalculation",
    packages=find_packages(),
    py_modules=["spartaCalculation"],
    version="0.0.16",
)
