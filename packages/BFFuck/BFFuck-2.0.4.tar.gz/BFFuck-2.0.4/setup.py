from setuptools import *
setup(
    name='BFFuck',
    version='2.0.4',
    url='https://github.com/none-None1/BFFuck',
    packages=['bffuck'],
    description='Makes Brainfucking Easier!',
    long_description=open("README.md").read(),
    entry_points={'console_scripts':['bffuck=bffuck:_cli']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Code Generators'
    ],
    long_description_content_type='text/markdown'
)
