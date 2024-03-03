import re

from setuptools import setup

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = ''
with open('django_app_router/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)  # type: ignore

readme = ''
with open('README.md') as f:
    readme = f.read()

packages = [
    'django_app_router',
]

setup(
    name='django-app-router',
    author='STACiA',
    url='https://github.com/staciax/django-app-router',
    project_urls={
        'Issue tracker': 'https://github.com/staciax/django-app-router/issues',
    },
    version=version,
    packages=packages,
    license='MIT',
    description='A simple Django app to route requests, Inspired by Next.js App Router.',
    long_description=readme,
    long_description_content_type='text/markdown',
    install_requires=requirements,
    python_requires='>=3.8.0',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
