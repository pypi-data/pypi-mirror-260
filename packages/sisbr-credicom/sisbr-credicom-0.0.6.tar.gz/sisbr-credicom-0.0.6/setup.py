from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='sisbr-credicom',
    version='0.0.6',
    license='MIT License',
    author='Gabriel Moreno',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='gabrielgoncalvesmoreno@credicom.com.br',
    keywords='sisbr',
    description=u'função login dos sistemas sicoob',
    packages=['credicom_rpa'],
    install_requires=['botcity-framework-base','cryptocode','pyodbc'],)