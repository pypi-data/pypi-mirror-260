from setuptools import setup

setup(
    name='burmethon',
    version='0.0.1',
    author='Pho Thin Maung',
    author_email='phothinmg@gmail.com',
    description='Burmese Calendar API in Python',
    packages=['burmesedate'],
    install_requires=['requests'],
    extras_require={
        'dev': ['pytest', 'pylint', 'coverage', 'black', 'genbadge'],
    },
    url="https://github.com/phothinmg/burmethon",

    project_urls={
        'Source Code': 'https://github.com/phothinmg/burmethon/tree/main/burmethon',
        'Bug Tracker': 'https://github.com/phothinmg/burmethon/issues',
    },
    license="Apache-2.0"
)
