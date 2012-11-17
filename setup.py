import os
from setuptools import setup


PACKAGE_NAME = 'django-granular-access'
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
README_FILEPATH = os.path.join(CURRENT_DIR, 'README.rst')
REQUIREMENTS_FILEPATH = os.path.join(CURRENT_DIR, 'requirements.txt')


def get_requirements():
    with open(REQUIREMENTS_FILEPATH) as fp:
        return fp.read().splitlines()


setup(
    name=PACKAGE_NAME,
    version=0.1,
    packages=['granular_access'],

    author='Kirill Sibirev',
    author_email='k.sibirev@gmail.com',
    url='https://github.com/l0kix2/django-granular-access',
    description='Flexible permission system for Django.',
    long_description=open(README_FILEPATH).read(),
    keywords='django permissions',
    install_requires=get_requirements(),
    license='MIT',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
)
