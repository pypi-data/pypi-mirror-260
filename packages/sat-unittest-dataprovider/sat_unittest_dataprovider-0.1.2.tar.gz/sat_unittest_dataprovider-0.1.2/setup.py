from setuptools import setup, find_packages

requirements = []
test_requirements = requirements + ['flake8', 'coverage', 'tox']    # 'mypy',
dev_requirements = test_requirements + ['build', 'twine']

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='sat_unittest_dataprovider',
    version='0.1.2',

    author="Markus",
    author_email="markus2110@gmail.com",
    description="Package to add a data_provider decorator to a function, to run the test with different values",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["test", "unittest", "data provider", "dataprovider", "test cases"],
    url="https://gitlab.com/markus2110-public/python/packages/unittest-dataprovider",

    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        'test': test_requirements,
        'dev': dev_requirements,
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.10'
)
