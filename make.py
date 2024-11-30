"""
FIXME: Improve this later. mypy also needs to be included in the linting.
"""

import sys
import shutil
import subprocess
import threading
import webbrowser


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


def serve():
    """Serve the documentation"""
    print("Serving documentation...")

    def start_server():
        subprocess.run("python -m http.server --directory build/docs", shell=True)

    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    webbrowser.open("http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    server_thread.join()


def run(args: list[str]):
    commands = {
        "html": docs,
        "lint": lint,
        "clean": clean,
        "test": test,
        "serve": serve,
    }
    if len(args) == 0:
        print_help()
        return

    func = commands.get(args[0])
    if func is None:
        print_help()
        return

    func()


def print_help():
    print("Usage: make.py <command>")
    print("Commands:")
    print("  html: Build the documentation")
    print("  lint: Run pylint")
    print("  clean: Clean up docs and build artifacts")
    print("  test: Run tests")
    print("  serve: Serve the documentation")


if __name__ == "__main__":
    run(sys.argv[1:])
