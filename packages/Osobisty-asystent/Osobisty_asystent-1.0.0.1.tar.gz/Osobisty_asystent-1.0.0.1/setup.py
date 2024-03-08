from setuptools import setup
setup(
    name='Osobisty_asystent',
    version='1.0.0.1',
    packages=['address_book'],
    entry_points={'console_scripts': ['personal-assistant = address_book.assistant:main']},
    package_data={'address_book': ["*.json"]},
)