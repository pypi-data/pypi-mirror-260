from setuptools import setup, find_packages

setup(
    name='plasma-fhir-client-py',
    version='0.0.8',
    author='Eric Morgan',
    author_email='plasmafhir@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'base64'
    ],
    tests_require=['pytest'],
    test_suite='tests',
    description='Plasma FHIR Client for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://plasmahealth.net',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)