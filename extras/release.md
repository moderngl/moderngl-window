
# Making a release

A reminder how to correctly create a release.
Ensuring all steps are followed will greatly increase
the chance of a successful release.
It's easy to forget one small thing ending up generating
more work. Let's try to avoid that!

## Version Numbers

We try to follow semantic versioning as much as possible: https://semver.org/spec/v2.0.0.html

## Steps

* Update `CHANGELOG.md`
* Change version number in `moderngl_window.__version__`
* Change version numbers in docs/conf.py (`version` and `release`)
* Change version in `setup.py`
* `rm -rf .tox` (Force env recreation)
* Run tests. Ensure it passes for `py35`, `py36`, `py37` and `pep8`.
  Run using `tox`.
* Create release on Github : https://github.com/moderngl/moderngl_window/releases with entries from `CHANGELOG.md`
* `python setup.py bdist_wheel`
* `twine upload dist/moderngl_window-<version>-py3-none-any.whl`
* Ensure docs are updated : https://moderngl-window.readthedocs.io/
* Ensure things look correct on PyPI : https://pypi.org/project/moderngl-window/

## Notes

The advantage of using `tox` is that the package is properly built
and installed in each python enviroment. This eliminates many common
issues related to package management.
