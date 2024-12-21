from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="graph_server",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=required,
    python_requires=">=3.12",
    entry_points={
        'console_scripts': [
            'graph-server=src.server:main',
        ],
    },
)
