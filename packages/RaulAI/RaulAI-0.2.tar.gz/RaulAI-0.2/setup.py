from setuptools import setup, find_packages

setup(
    name='RaulAI',
    version='0.2',
    description='Eine kurze Beschreibung deiner Bibliothek',
    author='Raul',
    packages=find_packages(),
    install_requires=[
        # Hier kannst du die Abhängigkeiten deiner Bibliothek auflisten
        'numpy',
        'pandas',
    ],
)