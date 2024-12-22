from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="graph_server",
    version="0.0.1",
    author="Mehrdad Rafiei",
    author_email="mehrdadr94@gmail.com", 
    description="A client-server application using ZMQ to process system commands and mathematical expressions",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=required,
    python_requires=">=3.12",
    entry_points={
        'console_scripts': [
            'graph-server=graph_server.server:main',
        ],
    },
)
