# Maintainer Note: How to publish the library
Make sure you are on the latest version of `main`:
1. `git checkout main`
2. `git pull`

Set a new valid version number (see below for details):
1. Update the version number in `pyproject.toml` to `X.Y.Z`
2. Update the version number in `svg_timeline.__init__.py` to the same value
3. Complete & rename the `[Unreleased]` section in `CHANGELOG.md`
4. `git add -u`
5. `git commit -m "New library version X.Y.Z"`
6. `git tag "X.Y.Z" -a "New library version X.Y.Z"`
7. `git push --follow-tags`
8. Create a new GitHub release

Run these commands manually to build and publish the library:
1. `poetry build`
   (build the .whl and .tar.gz packages)
2. `poetry publish -r testpypi`
   (publish to https://test.pypi.org/project/svg-timeline/ first, then check that everything is ok)
3. `poetry publish`
   (final publish to https://pypi.org/project/svg-timeline/)


## Allowed version numbers
[Semantic versioning](https://semver.org/) and [PEP 440](https://peps.python.org/pep-0440/#public-version-identifier)
have different requirements on version numbers.
This project aims to use version numbers that are valid according to both standards.
Effectively this allows versions of the following form:
```
N.N.N[-(a|b|rc)N][-postN][-devN]
```

Where:
- `N` is a shorthand for a positive integer
- `(x|y)` symbolize two allowed variants `x` and `y`
- `[]` denote optional parts
- (the other symbols are literal characters)
