from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ml_access_key_extractor',
    version='0.1.0',
    license='MIT License',
    author='Guillerme Rezende Manhaes',
    keywords='nota_fiscal',
    description='Biblioteca para extrair chave de acesso na nota fiscal em PDF',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={'access_key_extractor': ['*']},
    include_package_data=True,
    install_requires=[
        'pdfplumber',
        'scikit-learn>=0.24.0'
    ],
)
