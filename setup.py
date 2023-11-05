"""Installation procedure for HoPRe"""


from setuptools import setup, find_packages


setup(
    name="hopre-requirements",
    version="0.1.0",
    description="Required Python packages for HoPRe",
    author="Heewon Lee",
    author_email="pingpingy@kaist.ac.kr",
    packages=find_packages(include=["hopre"]),
)
