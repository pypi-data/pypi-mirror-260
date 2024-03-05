# Bitergia Analytics GrimoireELK backends

GrimoireELK backends installed in Bitergia Analytics:
- **public-inbox**: software for efficiently managing and archiving public mailing
lists using Git repositories.
- **Topicbox**: email discussion platform that facilitates organized group
communication through dedicated email groups.
- **Pontoon**: web-based localization platform that facilitates collaborative
translation of software and documentation

## Requirements

 * Python >= 3.8

You will also need some other libraries for running the tool, you can find the
whole list of dependencies in [pyproject.toml](pyproject.toml) file.

## Installation

There are several ways to install grimoire-elk-public-inbox on your system: packages or source 
code using Poetry or pip.

### PyPI

grimoire-elk-public-inbox can be installed using pip, a tool for installing Python packages. 
To do it, run the next command:
```
$ pip install grimoire-elk-public-inbox
```

### Source code

To install from the source code you will need to clone the repository first:
```
$ git clone https://github.com/bitergia-analytics/grimoirelab-elk-public-inbox
$ cd grimoirelab-elk-public-inbox
```

Then use pip or Poetry to install the package along with its dependencies.

#### Pip
To install the package from local directory run the following command:
```
$ pip install .
```
In case you are a developer, you should install grimoire-elk-public-inbox in editable mode:
```
$ pip install -e .
```

#### Poetry
We use [poetry](https://python-poetry.org/) for dependency management and 
packaging. You can install it following its [documentation](https://python-poetry.org/docs/#installation).
Once you have installed it, you can install grimoire-elk-public-inbox and the dependencies in 
a project isolated environment using:
```
$ poetry install
```
To spaw a new shell within the virtual environment use:
```
$ poetry shell
```

## License

Licensed under GNU General Public License (GPL), version 3 or later.
