from setuptools import setup, find_packages

setup(
    name="GooBa",
    version="0.1.0beta",
    packages=find_packages(),  # Automatically find all packages (subdirectories with __init__.py)
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
    install_requires=[          # List of dependencies
        # Add any required dependencies here, e.g., 'requests', 'flask'

    ],
    entry_points={              # Optional: define entry points for command-line scripts
        'console_scripts': [
            # 'gooba=GooBa.main:main',  # Example: Add a command line tool
        ],
    },
    author="Seth Linn Khant",
    author_email="sethlk2006@gmail.com",
    description="Gooba is a python frontend web framework inspired by Reactjs.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://yourprojecturl.com",
    classifiers=[
        #
    ],
    python_requires='>=3.6',
)
