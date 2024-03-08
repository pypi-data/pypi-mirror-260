import pathlib
from setuptools import setup, find_packages

setup (
    name="pyqtrapid",
    version="0.0.1",
    author="Eden Iyanda",
    author_email="edeniyanda@gmail.com",
    description="A Python package that simplifies the initiation of PyQt5 projects, providing a one-command solution to generate comprehensive starter files for quick and efficient project customization.",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    license=    "MIT License",
    project_urls={
        "Source": "https://github.com/edeniyanda/pyqtrapid.git",
    },

    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],

    install_requires=[
        'PyQt5',
    ],
    python_requires=">=3.6",
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pyqtrapid=pyqtrapid.cli:main',
        ],
    }
)

