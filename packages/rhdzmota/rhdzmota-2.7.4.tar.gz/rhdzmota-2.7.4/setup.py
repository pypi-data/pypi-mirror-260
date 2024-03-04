import os
from typing import Dict, List
from setuptools import setup, find_namespace_packages


CODEBASE_PATH = os.environ.get(
    "CODEBASE_PATH",
    default=os.path.join("src", "main"),
)

with open("requirements.txt", "r") as file:
    requirements = [line for line in file.read().splitlines() if line and not line.startswith("#")]

with open(os.path.join(CODEBASE_PATH, "rhdzmota", "VERSION"), "r") as file:
    version = file.read().strip()

with open("README.md") as file:
    readme = file.read()


def get_extras_requires(requirement_list: List[str]) -> Dict[str, List[str]]:
    extra_requires = {
        "default": set([]),
        "all": set([]),
    }
    for line in requirement_list:
        line_with_tag = ":" in line
        line_comment = line.strip().startswith("#")
        if line_comment or not line_with_tag:
            print("Skipping requirement line: ", line)
            continue
        requirement, _, tags = line.partition(":")
        clean_requirement = requirement.strip()
        # Register clean requirement with "all" tag
        extra_requires["all"] = extra_requires["all"].union({clean_requirement})
        # Register clean requirement with corresponding tags
        for tag in tags.split(","):
            clean_tag = tag.strip()
            extra_requires[clean_tag] = extra_requires.get(clean_tag, set([])).union({clean_requirement})
    # Add the default requirements into all tags
    for tag in extra_requires.keys():
        if tag in ["default", "all"]:
            continue
        extra_requires[tag] = extra_requires[tag].union(extra_requires["default"])
    return {
        tag: list(reqs)
        for tag, reqs in extra_requires.items()
    }


dependencies = get_extras_requires(requirement_list=requirements)

setup(
    name="rhdzmota",
    version=version,
    description="RHDZMOTA Package",
    long_description=readme,
    long_description_content_type='text/markdown',
    url="https://github.com/rhdzmota/package.rhdzmota.com",
    author="Rodrigo H. Mota",
    author_email="info@rhdzmota.com",
    packages=find_namespace_packages(where=CODEBASE_PATH),
    package_dir={
        "": CODEBASE_PATH
    },
    package_data={
        "": [
            os.path.join("iso3166", "datafiles", "*.json"),
        ]
    },
    entry_points={
        "console_scripts": [
            "rhdzmota=rhdzmota.cli:main",
        ]
    },
    install_requires=dependencies["default"],
    extras_require=dependencies,
    include_package_data=True,
    python_requires=">=3.8.10"
)
