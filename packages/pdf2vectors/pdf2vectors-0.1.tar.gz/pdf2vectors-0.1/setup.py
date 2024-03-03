from setuptools import setup, find_packages

setup(
    name='pdf2vectors',
    version='0.1',
    packages=find_packages(),
    author='Andres Garcia',
    author_email='garcicon45@gmail.com',
    description='A package to interact with vectors DB',
    long_description='A package to interact with vectors DB',
    long_description_content_type='text/markdown',
    url='https://github.com/ruteru/pdf2vectors',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'pdfplumber',
        'tensorflow',
        'requests',
        'pinecone-client'
    ],
)
