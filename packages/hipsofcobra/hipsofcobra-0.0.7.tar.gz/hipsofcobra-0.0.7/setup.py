from setuptools import setup, find_packages

VERSION = '0.0.7'
DESCRIPTION = 'A package for calculating the branching ratios of a scalar decaying to pi ' + \
              ' and K mesons from a coupled-channel analysis.'

with open('README.md', encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

# Setting up
setup(
    name="hipsofcobra",
    version=VERSION,
    author="Patrick Blackstone (@blackstonep)",
    author_email="<blackstonep924@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={
      'hipsofcobra': ['input/*.txt']
    },
    install_requires=['numpy'],
    keywords=['python', 'physics', 'hep'],
)
