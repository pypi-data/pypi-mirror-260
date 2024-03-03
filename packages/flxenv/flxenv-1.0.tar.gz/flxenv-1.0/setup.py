from setuptools import setup
from setuptools.command.install import install

setup(
    name='flxenv',
    version='1.0',
    description='Gestor de versiones de Flux',
    author='Jose Ignacio Rivero Costa',
    author_email='joseignacio@riverocosta.com',
    url='https://github.com/nachrivcost/flxenv',
    packages=['flxenv'],
    install_requires=[
        # Lista de dependencias requeridas
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
    entry_points={
        'console_scripts': [
            'flxenv = flxenv.main:main',
        ],
    },
)