from setuptools import setup, find_packages

setup(
    name="bc_sus_columnvalidation",
    #update your version number here
    version="0.9.2",
    package_dir={"": "src"},  # Tells setuptools that packages are under src
    packages=find_packages(where="src"),
    install_requires=[
        'pandas',
        'openpyxl'
    ]
)
