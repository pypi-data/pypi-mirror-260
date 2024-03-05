from setuptools import setup


def read_file(fname):
    with open(fname) as f:
        return f.read()


setup(
    name='pytest_testrail_results',
    description='A pytest plugin to upload results to TestRail.',
    long_description=read_file('README.rst'),
    version='1.0.2',
    author='Oleg_Miroshnychenko',
    author_email='miroshnychenko@dnt-lab.com',
    packages=[
        'pytest_testrail_results',
    ],
    package_dir={'': 'src'},
    install_requires=[
        'pytest>=7.2.0',
        'requests>=2.30.0',
    ],
    include_package_data=True,
    entry_points={'pytest11': ['pytest-testrail = pytest_testrail_results.conftest']},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
