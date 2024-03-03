"""
TruSTAR SDK distribution setup
"""
# ! /usr/local/bin/python3

from glob import glob
from setuptools import setup, find_packages

# read version
version_globals = {}
with open("trustar/version.py", encoding="utf-8") as fp:
    exec(fp.read(), version_globals)
version = version_globals['__version__']

setup(
    name='trustar',
    packages=find_packages(),
    version=version,
    author='TruSTAR Technology, Inc.',
    author_email='support@trustar.co',
    url='https://github.com/trustar/trustar-python',
    download_url=f'https://github.com/trustar/trustar-python/tarball/{version}',
    description='Python SDK for the TruSTAR REST API',
    license='MIT',
    install_requires=['json_log_formatter',
                      'python-dateutil',
                      'requests',
                      'configparser',
                      'PyYAML'
                      ],
    include_package_data=True,
    scripts=glob('trustar/examples/**/*.py') + glob('trustar/examples/*.py')
)
