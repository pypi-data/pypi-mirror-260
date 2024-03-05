from setuptools import setup, find_packages

setup(
    name="nexus-python",
    version="0.1.3",
    packages=find_packages(),
    install_requires=["requests>=2.25.1", "openai>=1.13.3"],
    author="Will Humble",
    author_email="w@astraanalytics.co",
    description="A simple interface for interacting with NexusDB.",
    keywords="database nexusdb",
    url="https://www.nexusdb.io/",
)
