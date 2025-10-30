from setuptools import setup, find_packages

setup(
    name="GooBa",
    version="0.1.5",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'watchdog',
        # 'pyPEG2',
        # 'pypeg',
    ],
    entry_points={
        'console_scripts': [
            # 'gooba-new=project_generator:create_project_structure',
        ],
    },
    author="Seth Linn Khant",
    author_email="sethlk2006@gmail.com",
    description="Gooba is a python frontend web framework inspired by Reactjs.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SethLK/GooBa",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.6',
)
