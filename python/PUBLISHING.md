# Publishing the library to PyPi

This library is published using flit. You only need to do this if you are the
library maintainer!

Before publishing, be sure to lint the code, and update the version number
in src/itech_serial/__init__.py

First, make a virtual environment to publish from:

    python3 -m venv .venv
    . .venv/bin/activate
    pip install flit

Next, build the project using flit, then upload it:

    flit build
    flit publish

Finally, the virtual enviroment can be removed:

    deactivate
    rm -rf .venv
