from setuptools import setup, find_packages

# read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

VERSION = '1.2.1'
DESCRIPTION = 'Visualization tool designed to analyze and illustrate the Lorenz Energy Cycle for atmospheric science.'

setup(
    name="lorenz_phase_space",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author="Danilo Couto de Souza",
    author_email="danilo.oceano@gmail.com",
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    keywords='conversion',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)
