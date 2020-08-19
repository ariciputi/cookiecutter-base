# Cookiecutter base

This is a base template for my own Python projects. It uses [cookiecutter](https://github.com/cookiecutter/cookiecutter) to
create the actual project structure out of the present template.

The template in itself is very basic and includes the common tools I'm used to
when I work with Python.

The template creates a `src`-layout project as described in the [pytest
docs](https://docs.pytest.org/en/stable/goodpractices.html#choosing-a-test-layout-import-rules).

The template uses [Poetry](https://python-poetry.org/) as packaging and
dependency manger, and it creates a virtualenv with the basic development tools
right inside the project's root directory (just because I like it so).

The development tools automatically installed in the virtualenv are:

- [ipython](https://ipython.org/)
- [pdbpp](https://github.com/pdbpp/pdbpp)
- [black](https://github.com/psf/black)
- [pylint](https://www.pylint.org/)
- [isort](https://pypi.org/project/isort/)
- [pre-commit](https://pre-commit.com/)
- [pytest](https://docs.pytest.org/en/stable/) along with [pytest-cov](https://pypi.org/project/pytest-cov/) and [pytest-randomly](https://pypi.org/project/pytest-randomly/)
- [coverage](https://pypi.org/project/coverage/)

Optionally you can add automatic documentation generation by adding
[portray](https://pypi.org/project/portray/) as an additional dependency. I know
`portray` is a little bit heavy on dependencies, but after all they are just
development dependencies and having documentantion automatically generated from
docstrings is way easier than any other alternative.

Eventually if you want to add some infosec-related dependencies you can. At the
moment only [bandit](https://pypi.org/project/bandit/) is supported but other
packages will be added soon.

## Caveat

Because the template itself creates a Python virtual environment, you cannot run
the template's tests in a usual virtualenv (if you do so, you end up with tests
installing project's dependencies in the template's virtualenv instead that in
the project's virtualenv). To avoid this issue you can find a Dockerfile in this
repository to run tests inside a container.

Please also note that this repository is not meant to be build to produce a
Python wheel as you would do with a standard Python package. This is just a
template to create an actual project. For this reason Poetry it is used here
just to install `black` and `pylint` which are useful during the template
development.

To run the tests build the docker images and run it:

```
$ docker build -t test_cookiecutter_base -f Dockerfile.tests .

$ docker run -it --rm test_cookiecutter_base:latest
```
