from setuptools import setup, find_packages 
from pathlib import Path 

this_directory = Path(__file__).parent 
long_description = (this_directory/ "README.md").read_text() 

setup(
    name='mutable-dev',
    version='0.1.7.7',
    author='Mutable',
    author_email='chase@mutability.ai',
    description='Success-based pricing SDK for LLM-based applications',
    packages=['mutable', 'mutable.helpers'],
    classifiers=['Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',],
python_requires='>=3.11',
long_description=long_description,
long_description_content_type='text/markdown'
)