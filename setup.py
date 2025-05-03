# setup.py
from setuptools import setup, find_packages

setup(
  name="chess_project",
  version="0.1",
  packages=find_packages(),  # this will pick up runner/ and database_utils/
  install_requires=[
    # list your pip dependencies here if you like
  ],
)
