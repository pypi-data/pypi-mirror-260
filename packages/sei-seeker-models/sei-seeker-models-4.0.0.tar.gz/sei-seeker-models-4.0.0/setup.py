from setuptools import setup, find_packages


with open("requirements.txt") as f:
    required = [line for line in f.read().splitlines() if not line.startswith("-")]

with open("VERSION") as f:
    version = f.read()

setup(
    name="sei-seeker-models",
    version=version,
    description="HYPERLABS",
    install_requires=required,
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.9",
)
