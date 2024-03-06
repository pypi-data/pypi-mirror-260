from setuptools import setup, find_packages

setup(
    name='aws_easy_tool',
    version='0.4.0',
    description='A Python package to facilitate daily tasks when using AWS.',
    author='Marcelo Eduardo Benencase',
    author_email='marcelo.benencase@gmail.com',
    url='https://github.com/mbenencase/py-aws',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'pydantic',
        'pydantic-settings',
        'tqdm',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'aws-easy-tool = awseasytool.module1:main',
        ],
    },
)
