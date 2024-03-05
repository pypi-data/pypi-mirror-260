from setuptools import setup, find_packages

setup(
    name='french_color_to_hex',
    version='0.1',
    packages=find_packages(),
    package_data={'french_color_to_hex': ['colors.json']},
    install_requires=[
        'unidecode'
    ],
)