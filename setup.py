import os
from distutils.core import setup


CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
README_FILEPATH = os.path.join(CURRENT_DIR, 'README.txt')


setup(
    name='django-granular-access',
    version='0.1',
    packages=[
        'granular_access',
        'granular_access.tests',
        'granular_access.migrations'
    ],
    author='Kirill Sibirev',
    author_email='k.sibirev@gmail.com',
    url='https://github.com/l0kix2/django-granular-access',
    description='Flexible permission system for Django.',
    long_description=open(README_FILEPATH).read(),
    keywords=['django', 'permissions'],
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
