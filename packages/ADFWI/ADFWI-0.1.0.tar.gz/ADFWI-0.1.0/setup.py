from setuptools import setup

setup(
    name="ADFWI",
    version="0.1.0",
    long_description="ADFWI",
    long_description_content_type="text/markdown",
    packages=["adfwi"],
    install_requires=["numpy",  "h5py", "matplotlib", "pandas"],
)
