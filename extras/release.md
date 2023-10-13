
# Making a release

A reminder how to correctly create a release. Ensuring all steps are followed will greatly increase
the chance of a successful release. It's easy to forget one small thing ending up generating
more work. Let's try to avoid that!

## Version Numbers

We try to follow semantic versioning as much as possible: https://semver.org/spec/v2.0.0.html

## Steps

* Update `CHANGELOG.md`
* Change version number in `moderngl_window.__version__`
* Change version numbers in docs/conf.py (`version` and `release`)
* Change version in `pyproject.toml`
* Run `pytest` locally and also verify tests have passed in github actions
* Create release on Github : https://github.com/moderngl/moderngl-window/releases with entries from `CHANGELOG.md`
  * `python -m build . --wheel --sdist --outdir dist/`
  * `twine upload dist/moderngl-window-<version>-py3-none-any.whl`
  * `twine upload dist/moderngl-window-<version>.tar.gz`
* Ensure docs are updated : https://moderngl-window.readthedocs.io/
* Ensure things look correct on PyPI : https://pypi.org/project/moderngl-window/
