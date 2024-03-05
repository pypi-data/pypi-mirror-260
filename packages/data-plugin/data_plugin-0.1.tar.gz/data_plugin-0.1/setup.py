from setuptools import setup, find_packages

setup(
    name='data_plugin',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'typer',
        # Add any other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'plug=plug:app',
        ],
    },
)
