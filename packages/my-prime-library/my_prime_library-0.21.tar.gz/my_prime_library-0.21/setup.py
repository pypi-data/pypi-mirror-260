from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='my_prime_library',
    version='0.021',  
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'my_prime_library=my_prime_library.sieve:main',
        ],
    },
    description='A Python library implementing the Sieve of Eratosthenes algorithm for prime number generation.',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
