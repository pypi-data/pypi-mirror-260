from setuptools import setup, find_packages

install_requires = ["bitarray"]

setup(
    name="olympiad_data_structures",
    version="0.0.5",
    install_requires=install_requires,
    use_scm_version=True,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
)
