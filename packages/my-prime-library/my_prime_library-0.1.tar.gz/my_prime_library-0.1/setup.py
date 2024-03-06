from setuptools import setup, find_packages

setup(
    name='my_prime_library',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'my_prime_library=my_prime_library.sieve:main',
        ],
    },
    description='A Python library implementing the Sieve of Eratosthenes algorithm for prime number generation.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
