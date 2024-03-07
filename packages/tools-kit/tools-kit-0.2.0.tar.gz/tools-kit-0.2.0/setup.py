from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='tools-kit',
    version='0.2.0',
    license='MIT License',
    author='Mateus Laurentino de Andrade',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='mateus_laurentino@outlook.com',
    keywords='tools kit',
    description=u'Gerenciador para facilitar o desenvolvimento padronizado',
    packages=['tools_rest'],
    install_requires=['django', 'djangorestframework'],)