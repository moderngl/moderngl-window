"""
FIXME: Improve this later. mypy also needs to be included in the linting.
"""

import sys
import shutil
import subprocess


def docs():
    """Sphinx documentation"""
    print("Building documentation...")
    subprocess.run("sphinx-build docs build/docs", shell=True)


def clean():
    """Clean up docs and build artifacts"""
    print("Cleaning up...")
    shutil.rmtree("build", ignore_errors=True)


def lint():
    """Run pylint"""
    print("Running pylint...")
    subprocess.run("ruff check", shell=True)


def test():
    """Run tests"""
    print("Running tests...")
    subprocess.run("pytest tests/", shell=True)


def run(args: list[str]):
    commands = {
        "html": docs,
        "lint": lint,
        "clean": clean,
        "test": test,
    }
    if len(args) == 0:
        print("Usage: make.py <command>")
        return

    func = commands.get(args[0])
    if func is None:
        print(f"Unknown command: {args[0]}")
        return

    func()


if __name__ == "__main__":
    run(sys.argv[1:])
