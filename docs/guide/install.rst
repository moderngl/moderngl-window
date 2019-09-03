
Installation
============

Installing with pip
-------------------

moderngl_window is available on PyPI::

    pip install moderngl_window
    # Package name with dash also works
    pip install moderngl-window

If installing the package globally (into site-packages), consider
using ``--user`` option::

    pip install --user moderngl_window


Installing from source
----------------------

.. code:: bash

    # clone repo (optionally clone over https)
    git clone git@github.com:moderngl/moderngl_window.git
    cd moderngl_window

    # Create your virtualenv and activate
    # We assume the user knows how to work with virtualenvs

    # Install moderngl_window in editable mode
    pip install -e .

Installing the package in editable mode will make you able
to run tests and examples. We highly recommend using
virtualenvs.

Optional dependencies
---------------------

We try to have as few requirements as possible and instead offer
optional dependencies. You can create your own window types
and loaders and don't want to force installing unnecessary dependencies.

By default we install pyglet as this is the default window type
as it small and pretty much work out of the box on all platforms.

Installing dependencies for optional window type::

    pip install moderngl_window[PySide2]
    pip install moderngl_window[pyqt5]
    pip install moderngl_window[glfw]
    pip install moderngl_window[PySDL2]

Optional dependencies for loaders::

    # Wavefront / obj loading
    pip install moderngl_window[pywavefront}
    # STL loading
    pip install moderngl_window[trimesh]

Running examples
----------------

Assuming you installed from source you should be able to run the examples
in the `examples` directory directly after installing the dev requirements
in the root of the project::

    pip install -r requirements.txt

Running tests
-------------

Install test requirements::

    pip install -r tests/requirements.txt

Run tests with ``tox``::

    # Run for specific enviroment
    tox -e py35
    tox -e py36
    tox -e py37

    # pep8 run
    tox -e pep8

    # Run all enviroments
    tox
