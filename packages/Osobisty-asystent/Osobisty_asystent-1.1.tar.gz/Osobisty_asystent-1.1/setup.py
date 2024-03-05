from setuptools import setup
setup(
    name='Osobisty_asystent',
    version='1.1',
    packages=['address_book'],
    package_data={
        '': ['*.json'],
    },
    entry_points={
        'console_scripts': [
            'personal-assistant = address_book.assistant:main'
        ]
    }
)