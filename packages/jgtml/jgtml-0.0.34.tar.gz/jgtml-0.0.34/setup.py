#!/usr/bin/env Python
"""
jgtml
"""

from setuptools import find_packages, setup

from jgtml import __version__ as version

INSTALL_REQUIRES = [
    "pandas>=0.25.1",
    "python-dotenv>=0.19.2",
    #'kaleido>=0.2.1',
    "matplotlib>=3.3.1",
    "plotly>=5.18.0",
    "jgtpy>=0.3.36",
    "mplfinance>=0.12.10b0",
    "scipy>=1.7.3",
    "panel>=1.3.8",
    "seaborn>=0.13.2",
]

EXTRAS_DEV_LINT = [
    "flake8>=3.6.0,<3.7.0",
    "isort>=4.3.4,<4.4.0",
]

EXTRAS_DEV_TEST = [
    "coverage",
    "pytest>=3.10",
]

EXTRAS_DEV_DOCS = [
    "readme_renderer",
    "sphinx",
    "sphinx_rtd_theme>=0.4.0",
    "html2text>=2020.1.16",
    "html2markdown>=0.1.7",
]

setup(
    name="jgtml",
    version=version,
    description="JGTrading Data maker' Dataframes",
    long_description=open("README.rst").read(),
    author="GUillaume Isabelle",
    author_email="jgi@jgwill.com",
    url="https://github.com/jgwill/jgtml",
    packages=find_packages(include=["jgtml"], exclude=["*test*"]),
    # packages=find_packages(include=['jgtml', 'jgtml.forexconnect', 'jgtml.forexconnect.lib', 'jgtml.forexconnect.lib.windows', 'jgtml.forexconnect.lib.linux'], exclude=['*test*']),
    install_requires=INSTALL_REQUIRES,
    entry_points={
        "console_scripts": ["jgtmlcli=jgtml.jgtmlcli:main"],
    },
    extras_require={
        "dev": (EXTRAS_DEV_LINT + EXTRAS_DEV_TEST + EXTRAS_DEV_DOCS),
        "dev-lint": EXTRAS_DEV_LINT,
        "dev-test": EXTRAS_DEV_TEST,
        "dev-docs": EXTRAS_DEV_DOCS,
    },
    license="MIT",
    keywords="data",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.7.16",
    ],
)
