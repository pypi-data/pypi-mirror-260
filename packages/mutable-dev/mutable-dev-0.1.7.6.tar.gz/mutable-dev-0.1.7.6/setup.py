from setuptools import setup, find_packages 
setup(
    name='mutable-dev',
    version='0.1.7.6',
    author='Mutable',
    author_email='chase@mutability.ai',
    description='Success-based pricing SDK for LLM-based applications',
    packages=['mutable', 'mutable.helpers'],
    classifiers=['Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',],
python_requires='>=3.11',
)