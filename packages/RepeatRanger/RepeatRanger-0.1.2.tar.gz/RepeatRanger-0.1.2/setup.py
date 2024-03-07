import re

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = None
for line in open("./src/RepeatRanger/__init__.py"):
    m = re.search("__version__\s*=\s*(.*)", line)
    if m:
        version = m.group(1).strip()[1:-1]  # quotes
        break
assert version

setup(
    name="RepeatRanger",
    version=version,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={"": ["README.md"]},
    python_requires=">=3.6",
    include_package_data=True,
    scripts=[],
    license="BSD",
    url="https://github.com/ad3002/RepeatRanger",
    author="Aleksey Komissarov",
    author_email="ad3002@gmail.com",
    description="De Novo Repeat Annotation Tool for Assembled Genomes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "tqdm",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    entry_points={
        'console_scripts': [
            'repeatranger = RepeatRanger.prototype_assembly:main',
        ],
    },
)
