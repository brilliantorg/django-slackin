import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-slackin',
    version='0.0.2',
    packages=['slackin'],
    include_package_data=True,
    license='MIT License',
    description='Django integration with a public slack organization (inspired by https://github.com/rauchg/slackin)',
    long_description=README,
    url='https://github.com/brilliantorg/django-slackin',
    author='Caleb Rash',
    author_email='caleb@brilliant.org',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
