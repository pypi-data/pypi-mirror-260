from setuptools import find_packages, setup
setup(
    packages=find_packages(include=['FSRray']),
    version='1.1.0',
    name='FSRray',
    url="https://github.com/Aightech/pyFSRray",
    description='Python library to communicate with the FSR array',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Alexis Devillard',
    license='MIT',
    install_requires=['pyserial'],
    setup_requires=['pytest-runner', 'pyserial'],
    tests_require=['pytest==4.4.1', 'pyserial'],
    test_suite='tests',
)