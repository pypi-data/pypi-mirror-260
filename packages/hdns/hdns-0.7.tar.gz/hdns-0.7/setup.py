from setuptools import setup, find_packages

setup(
    name='hdns',
    version='0.7',
    description='A simple library to handle Hetzner DNS API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='shadi andrew',
    url='https://github.com/yourusername/your_package_name',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
