import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hyron",
    version="0.2.1",
    author="Jacob Neil Taylor",
    author_email="me@jacobtaylor.id.au",
    description="The Network Security Policy Automation Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jacobneiltaylor/hyron",
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    package_data={
        "hyron": [
            "builtin/*.yaml",
            "assets/*"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",  # noqa
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "requests",
        "metaloader",
        "plugable",
        "py-radix",
        "py-mini-racer",
    ],
)
