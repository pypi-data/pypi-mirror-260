from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='pyfractions',
    version='0.1.0',
    description='A Python library for working with fractions',
    long_description=long_description, 
    long_description_content_type='text/markdown',  # Set the content type of the long description
    author='Atul kushwaha',
    author_email='atulkushwaha2008@gmail.com',
    url='https://github.com/coderatul/fraction',
    packages=['pyfractions'],
    install_requires=[],
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='fraction math',
    project_urls={
        'Source': 'https://github.com/coderatul/fraction',
        'Tracker': 'https://github.com/coderatul/fraction/issues',
    },
)
