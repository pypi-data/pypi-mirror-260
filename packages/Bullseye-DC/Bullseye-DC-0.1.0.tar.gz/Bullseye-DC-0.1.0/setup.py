from setuptools import setup
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_URL = "https://github.com/purebluen73/Bullseye-DC"
DESC_REPLACEMENTS = {
    ".. _LICENSE: LICENSE":
    ".. _LICENSE: {}/blob/master/LICENSE".format(REPO_URL),
}


def long_description():
    with open(os.path.join(SCRIPT_DIR, "README.rst"), encoding='utf-8') as f:
        lines = f.read().splitlines()
    result = []
    for line in lines:
        result.append(DESC_REPLACEMENTS.get(line, line) + "\n")
    return "".join(result)


LICENSE = """\
License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)\
"""


setup(
    name="Bullseye-DC",
    version="0.1.0",
    description=(
        "A free program for performing tasks with Discord."
    ),
    author="purebluen73",
    author_email="purebluen73@gmail.com",
    license="GNU General Public License v3 or later (GPLv3+)",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Internet", LICENSE,
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="discord",
    packages=["Bullseye"],
    entry_points={
        "console_scripts": [
            "Bullseye=Bullseye:main",
        ],
    },
    install_requires=[
        "Pillow>=4.1.1",
        "requests>=2.18.1,<3",
        "librecaptcha[gtk]>=0.6.3,<1",
        "keyring>=17.0.0",
    ],
    python_requires=">=3.5",
)
