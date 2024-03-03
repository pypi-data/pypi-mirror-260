from setuptools import setup, find_packages
setup(
    name='envarify',
    version='0.0.0',
    author='Vadim Titov',
    author_email='titov.hse@gmail.com',
    description='Environment variables parsing and validation using python type hints',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

