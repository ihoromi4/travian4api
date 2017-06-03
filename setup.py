from setuptools import setup

import travian4api

setup(
    name='travian4api',
    version=travian4api.__version__,
    url='https://bitbucket.org/igoromi4/travian4api',
    license='BSD',
    author='Ihor Omelchenko',
    author_email='counter3d@gmail.com',
    description='API for Travian Legends browser game',
    platforms='any',
    install_requires=[
        'requests',
        'html5lib',
        'bs4'
    ],
    packages=[
        'travian4api',
        'travian4api.travparse',
        'travian4api.travparse.parsebuild',
        'travian4api.village',
        'travian4api.village.buildings'
    ],
    package_dir={'travian4api': 'travian4api'},
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
