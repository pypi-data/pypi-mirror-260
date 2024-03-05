from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt', 'r') as req:
        return req.read().splitlines()

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='SolTg',
    version='0.0.3',
    packages=find_packages(),
    include_package_data=True,  # This tells setuptools to include files listed in MANIFEST.in
    author = "Konstantin Britikov",
    author_email = "BritikovKI@Gmail.com",
    description = "Test generation for Solidity in Foundry format (https://github.com/foundry-rs/foundry).",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    # If needed, specify explicit paths
    install_requires=read_requirements(),
    package_data={
        'my_package': ['./lib/*'],
    },
    # Or for distribution-wide resources
    data_files=[('lib', ['lib/tgnonlin', 'lib/tgnonlin_linux', 'lib/run_solcmc', 'lib/docker_solcmc_updated'])],
    entry_points={
        'console_scripts': [
            'solTg=solidity_testgen.RunAll:main',
        ],
    },
)
