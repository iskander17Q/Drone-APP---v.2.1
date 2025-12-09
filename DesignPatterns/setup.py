"""Setup configuration for Design Patterns module."""
from setuptools import setup, find_packages

setup(
    name='design-patterns',
    version='1.0.0',
    description='Reference implementations of 9 design patterns: Creational, Structural, and Behavioral',
    author='Drone APP Development',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.10',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
