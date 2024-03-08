import os
import sys
import warnings

from setuptools import setup


with open("README.md", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()


def obsolete_error():
    error_message = "\n".join(
        [
            "The 'sinaraml_cli' PyPI package is deprecated, use 'sinaraml'",
            "rather than 'sinaraml_cli_host' for installation with pip."
        ]
    )

    raise SystemExit(error_message)


if __name__ == "__main__":
    sdist_mode = len(sys.argv) == 2 and sys.argv[1] == "sdist"

    if not sdist_mode:
        obsolete_error()

    setup(
        description="deprecated sinaraml_cli package, use sinaraml instead",
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        name="sinaraml_cli",
        version="v2024.03.07",
        author="sinaraml",
        author_email = "sinaraml.official@gmail.com",
        url="https://github.com/4-DS/sinaraml_cli",
        license_files = ('LICENSE',),
        keywords = ["cli", "sinaraml"],
        classifiers = [
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
        ]
    )