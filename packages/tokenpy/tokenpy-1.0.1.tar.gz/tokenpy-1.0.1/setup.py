from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="tokenpy",
    version='1.0.1',
    author='byte-my-code',
    author_email='lamaswaroop@gmail.com',
    description='Check your wallet balance from the cli',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/lachenlama/tokenpy',
    packages=find_packages(),
    install_requires=[
        'argparse',
        'web3',
    ],
    scripts=['script.py'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)