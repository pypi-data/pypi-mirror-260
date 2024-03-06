import re

import setuptools

with open("src/query_state_lib/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="query-blockchain-state-lib",
    version=version,
    author="Viet-Bang Pham",
    author_email="phamvietbang2965@gmail.com",
    description="Query EVM state data by batch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Centic-io/query-blockchain-state-lib",
    project_urls={
        "Bug Tracker": "https://github.com/Centic-io/query-blockchain-state-lib",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'web3>=6.0.0',
        'requests<=3.0.0',
        'pbkdf2<=1.3',
    ]
)