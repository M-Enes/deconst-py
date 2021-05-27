#!/usr/bin/env python3
from distutils.core import setup

setup(name="deconst.py",
      version="0.8.1",
      description="Simple command line tool that deconsts Python files.",
      long_description="""
  deconst-py is a command line tool for remove constant variables and
  replace them to their values.
  Coding in Python for deconst Python codes.
  Made by Muhammed Enes Karaca https://github.com/m-enes.""",
      author="Muhammed Enes Karaca",
      author_email="karaca.1453.@gmail.com",
      url="https://github.com/m-enes/deconst-py",
      scripts=['bin/deconst.py'],
      license="Licensed under the GPL version 3",
      )
