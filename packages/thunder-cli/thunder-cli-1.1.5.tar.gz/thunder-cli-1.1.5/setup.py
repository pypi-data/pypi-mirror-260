from setuptools import setup, find_packages

setup(
    name="thunder-cli",
    version="1.1.5",
    package_dir={"": "src"},  # Specify the root directory for packages
    packages=find_packages(where="src"),  # Tell setuptools to find packages under src
    include_package_data=True,  # Include other files specified in MANIFEST.in
    install_requires=["Click", "requests", "cryptography", "common"],
    entry_points={"console_scripts": ["thunder=thunder.thunder:cli"]},
)

# delete old dist folder first, and increment version number
# to build: python setup.py sdist bdist_wheel
# to distribute: twine upload dist/* --repository testpypi
# to install: pip install thunder-client
