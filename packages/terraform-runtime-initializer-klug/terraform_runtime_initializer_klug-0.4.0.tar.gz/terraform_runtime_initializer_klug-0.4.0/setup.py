from setuptools import setup, find_packages

setup(
    name='terraform_runtime_initializer_klug',
    version='0.4.0',
    packages=find_packages(),
    package_data={'terraform_runtime_initializer_klug': ['templates/*']},
    entry_points={
        'console_scripts': [
            'trik=terraform_runtime_initializer_klug.initializer:main',
        ],
    },
)

