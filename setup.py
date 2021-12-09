from setuptools import find_packages, setup

with open('VERSION') as version_file:
    version = version_file.read().strip()

setup(
    name='hyperia-python-sdk',
    version=version,
    packages=find_packages(exclude=["build", "dist", "hyperia-client-sdk.egg-info*", "test*"]),
    description='Hyperia Client SDK',
    install_requires=["requests",
                      "websocket-client"]
)
