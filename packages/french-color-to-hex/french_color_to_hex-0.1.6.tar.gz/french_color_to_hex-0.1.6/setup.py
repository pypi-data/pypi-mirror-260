from setuptools import setup, find_packages

setup(
    name='french_color_to_hex',
    py_modules=['french_color_to_hex'],
    version='0.1.6',
    packages=find_packages(),
    package_data={'french_color_to_hex': ['colors.json']},
    install_requires=[
        'unidecode'
    ],
)