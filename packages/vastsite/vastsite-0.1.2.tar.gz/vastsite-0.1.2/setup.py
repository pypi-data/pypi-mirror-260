from setuptools import setup, find_packages

setup(
    name='vastsite',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'Flask',
    ],
    author='Mingde Yang',
    author_email='yangsilicon9@gmail.com',
    description='A simple Python package to simplify Flask web app development.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your_username/flask_easy',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
