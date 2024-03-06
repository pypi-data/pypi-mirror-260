from setuptools import setup, find_packages

with open ('readme.txt','r') as file:
    description = file.read()

setup(
    name='enaCLI',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'argparse',
        'pandas',
        'lxml',
    ],
    entry_points={
        'console_scripts': [
            'enaCLI = enaCLI.__main__:main',
        ],
    },
    author='Khadim GUEYE',
    author_email='gueye.kgy@gmail.com',
    description='This script facilitates the submission of projects, samples, runs, assemblies, and other analyses to the public repository ENA (European Nucleotide Archive). It also assists in validating AMR (Antimicrobial Resistance) antibiograms before submission.',
    url='https://github.com/KhadimGueyeKGY/ena-CLI',
    long_description = description,
    long_description_content_type = 'text/markdown',
)
