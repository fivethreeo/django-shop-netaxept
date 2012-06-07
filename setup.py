from setuptools import setup, find_packages
import os

import shop_netaxept

CLASSIFIERS = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
]

setup(
    name='django-shop-netaxept',
    version=shop_netaxept.get_version(),
    description='This is a payment module for django-shop using Netaxept',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author='Oyvind Saltvik',
    author_email='oyvind.saltvik@gmail.com',
    url='http://github.com/fivethreeo/django-shop-netaxept/',
    packages=find_packages(),
    package_data={
        'djnetaxept': [
            'static/shop_netaxept/*',
            'locale/*/LC_MESSAGES/*',
        ]
    },
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False,
    install_requires=['django-netaxept']
)
