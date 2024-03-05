from setuptools import setup, find_packages

VERSION = '1.0.6' 
DESCRIPTION = 'GAUSSian BEam ANalysis package'

# Setting up the package
setup(
        name="gaussbean", 
        version=VERSION,
        author="Leah Hartman",
        author_email="<leah.ghartman@gmail.com>",
        description=DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages needed
        keywords=['python', 'gaussian', 'laser'],
        classifiers= []
)
