from setuptools import setup

import travianapi

setup(
    name='travianapi',
    version=travianapi.__version__,
    url='https://bitbucket.org/igoromi4/travian-legends-api',
    license='BSD',
    author='Igor Omelchenko',
    author_email='counter3d@gmail.com',
    description='API for Travian Legends browser game',
    platforms='any',
    install_requires=[
        'requests',
        'bs4'
    ],
    packages=[
        'travianapi',
        'travianapi.travparse',
        'travianapi.travparse.parsebuild',
        'travianapi.village',
        'travianapi.village.buildings'
    ],
    package_dir={'travianapi': 'travianapi'},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment:: Web Environment',
        'Intended Audience:: Developers',
        'Operating System:: OS Independent',
        'Programming Language:: Python',
        'Topic:: Software Development:: Libraries:: Python Modules'
    ]
)
