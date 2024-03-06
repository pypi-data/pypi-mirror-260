from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()


setup(name='biblioteca_enigma',
    version='0.0.1',
    license='MIT License',
    author='Laura Pontiroli Machado',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='laahpontiroli@gmail.com',
    keywords='enigma',
    description=u'Biblioteca enigma para aps de Algebra Linear',
    packages=['enigma'],
    install_requires=['numpy'],)