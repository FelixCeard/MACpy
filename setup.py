from setuptools import setup, find_packages

setup(
    name='MACpy',
    version='0.1.1',
    author='Felix Ceard-Falkenberg',
    author_email='felix@falkenbergs.de',
    packages=['mac', 'slim'],
    package_data={'': ['MAC.jar']},
    include_package_data=True,
    description='A wrapper for the MAC algorithm',
    install_requires=[
        'pandas'
    ],
)
