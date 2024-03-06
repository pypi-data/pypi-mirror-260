from setuptools import setup, find_packages

setup(
    name='terraform_runtime_initializer_klug',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'trik=terraform_runtime_initializer_klug.initializer:main',
        ],
    },
)

