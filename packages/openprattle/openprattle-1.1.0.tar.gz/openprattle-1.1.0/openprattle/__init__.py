"""A wrapper for accessing the pybel library and obabel command-line tools"""

import sys
from pathlib import Path

# Version information.
major_version = 1
minor_version = 1
revision = 0
prerelease = None

development = prerelease is not None

__version__ = "{}.{}.{}{}".format(major_version, minor_version, revision,"-pre.{}".format(prerelease) if development else "")
__author__ = "Oliver S. Lee"

# Set-up openbabel.
#
# This must be done prior to an obabel import.
#     
# When frozen with pyinstaller we take a version of the openbabel C library with us (along with the relevant python bindings of course).
# This library is split into several .so files corresponding to the various formats obabel supports, and while the main libopenbabel.so
# file is found automatically, these supplementary library files are not.
#
# So, when we are frozen, we manually set the location of these library files so openbabel will work.
# If we are not frozen we do not do this as we expect openbabel to be correctly configured.
# The sys attribute 'frozen' is our flag, '_MEIPASS' is the dir location.
# https://pyinstaller.readthedocs.io/en/stable/runtime-information.html#run-time-information
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    frozen = True
else:
    frozen = False

openbabel_version = "3.1.0"
if frozen:
    import os
    # We need to tell openbabel where its library components are.
    os.environ['BABEL_LIBDIR'] = str(Path(sys._MEIPASS, "openbabel", "lib", openbabel_version))
    
    # And also data.
    os.environ['BABEL_DATADIR'] = str(Path(sys._MEIPASS, "openbabel", "data", openbabel_version))

# Convenience imports.
from .babel import Openbabel_converter, HAVE_PYBEL, formats
