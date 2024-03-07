from setuptools import setup, find_packages
def requirements_from_file(file_name):
    return open(file_name).read().splitlines()
 
setup(
    name = "mlvault", 
    packages = find_packages(),
    version="0.0.28",
    author="MLVault",
    install_requires=requirements_from_file("requirements.txt"),
    entry_points={
        "console_scripts": [
            "mlvcli = mlvault.cli:main"
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.10',
    ]
)
