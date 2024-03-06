from pathlib import Path

from setuptools import find_packages, setup

excludes = (
    "*test*",
    "*local_settings*",
)


def requires(filename: str):
    return open(filename, encoding="utf-8").read().splitlines()


setup(
    name="mmpy_bot_mk2",
    # Updated by publish workflow
    version=Path(__file__)
    .parent.joinpath("mmpy_bot_mk2/version.txt")
    .read_text(encoding="utf-8")
    .rstrip(),
    author="Alex Tzonkov",
    author_email="anton.ohontsev@gmail.com",
    license="MIT",
    description="A python based bot for Mattermost with its own webhook server.",
    keywords="chat bot mattermost",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/movax01h/mmpy_bot_mk2",
    python_requires=">=3.8",
    platforms=["Any"],
    packages=find_packages(exclude=excludes),
    install_requires=requires("requirements.txt"),
    extras_require={"dev": requires("dev-requirements.txt")},
    package_data={"mmpy_bot_mk2": ["mmpy_bot_mk2/version.txt"]},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "mmpy_bot_mk2 = mmpy_bot_mk2.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
