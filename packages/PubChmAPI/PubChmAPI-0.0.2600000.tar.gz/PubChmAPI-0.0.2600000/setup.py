from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='PubChmAPI',
    version='0.0.2600000',
    description='This Python package, PubChemAPI, simplifies the interaction with the PubChem database, allowing users to seamlessly retrieve information related to compounds, substances, assays, proteins, genes, and more. Whether you\'re a researcher, scientist, or developer, this package provides an easy-to-use interface to access a wealth of information stored in PubChem.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://github.com/ahmed1212212/PubChemAPI.git',
    author='Ahmed Alhilal',
    author_email='aalhilal@udel.edu',
    license='MIT',
    classifiers=classifiers,
    keywords='cheminformatics',
    packages=find_packages(),
    install_requires=['requests']
)

