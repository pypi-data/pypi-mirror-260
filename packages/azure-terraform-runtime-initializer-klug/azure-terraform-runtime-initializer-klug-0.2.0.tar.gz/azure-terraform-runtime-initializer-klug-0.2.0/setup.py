from setuptools import setup, find_packages

setup(
    name='azure-terraform-runtime-initializer-klug',
    version='0.2.0',
    packages=find_packages(),
    package_data={'azure_terraform_runtime_initializer_klug': ['templates/*']},
    entry_points={
        'console_scripts': [
            'trik=azure_terraform_runtime_initializer_klug.initializer:main',
        ],
    },
)

