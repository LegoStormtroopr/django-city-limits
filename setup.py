import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-limits',
    version="0.0.6",
    packages=find_packages(),
    include_package_data=True,
    license='GPLv3 License',
    description="",
    long_description=README,
    url='https://github.com/LegoStormtroopr/django-limits/',
    author='Samuel Spencer',
    author_email='sam@aristotlemetadata.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords='django limit objects',
    install_requires=['django'], # I mean obviously you'll have django installed if you want to use this.
)