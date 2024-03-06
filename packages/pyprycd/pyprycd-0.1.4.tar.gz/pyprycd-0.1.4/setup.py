#!/usr/bin/env python
from pathlib import Path

from setuptools import setup, find_packages
from pyprycd import __version__
this_directory = Path(__file__).parent

setup_args = dict(
    name='pyprycd',
    # Add Packages
    packages=find_packages('pyprycd'),
    package_dir={'pyprycd': ''},
    include_package_data=True,
    version=__version__,
    license='MIT',
    description='An unofficial Python Client for the PRYCD API for Real Estate Analysis.',
    author='Charles S. Givre',
    author_email='charles@geniza.ai',
    url='https://github.com/geniza-ai/pyprycd',

    long_description = (this_directory / "README.md").read_text(encoding='utf-8'),
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: SQL',
        'Operating System :: OS Independent',
        'Topic :: Internet'
    ],
    install_requires=open('requirements.txt', encoding="utf-8").read().splitlines(),
)


def main() -> None:
    """
    Runs the setup of PyPryCD package.
    :return: Nothing
    """
    setup(**setup_args)


if __name__ == '__main__':
    main()
