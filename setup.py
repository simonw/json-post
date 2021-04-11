from setuptools import setup
import os

VERSION = "0.2a0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="json-post",
    description="Tool for posting JSON to an API, broken into pages",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/json-post",
    project_urls={
        "Issues": "https://github.com/simonw/json-post/issues",
        "CI": "https://github.com/simonw/json-post/actions",
        "Changelog": "https://github.com/simonw/json-post/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["json_post"],
    entry_points="""
        [console_scripts]
        json-post=json_post.cli:cli
    """,
    install_requires=["click", "httpx"],
    extras_require={"test": ["pytest"]},
    tests_require=["json-post[test]"],
    python_requires=">=3.6",
)
