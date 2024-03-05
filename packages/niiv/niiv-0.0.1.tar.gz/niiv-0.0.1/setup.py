from setuptools import setup, find_packages

setup(
    name='niiv',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'torch',
        'DISTS_pytorch',
        'lpips',
        'numpy',
    ],
    # Other metadata
    author='Anonymous Anonymous',
    author_email='anonymous@anonymous.com',
    description='Self-Supervised Neural Implicit Volume Reconstruction',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # This is important for a proper display on PyPI
    url='https://niiv.net',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
