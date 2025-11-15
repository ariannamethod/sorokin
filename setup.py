"""Setup script for sorokin package."""

from setuptools import setup, find_packages
from pathlib import Path
import re

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

# Read version from package
version_file = Path(__file__).parent / "src" / "sorokin" / "__init__.py"
version_match = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', version_file.read_text(), re.MULTILINE)
version = version_match.group(1) if version_match else "0.0.0"

setup(
    name="sorokin",
    version=version,
    author="Sorokin Project",
    description="A prompt autopsy engine for analyzing and dissecting LLM prompts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ariannamethod/sorokin",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "sorokin=sorokin.cli:main",
        ],
    },
    install_requires=[
        # No external dependencies for now - using only standard library
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ],
    },
)
