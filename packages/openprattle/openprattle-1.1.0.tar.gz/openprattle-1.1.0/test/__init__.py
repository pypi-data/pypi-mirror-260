"""Unit tests for openprattle"""

from pathlib import Path

from openprattle.babel import Pybel_converter, Obabel_converter, formats, Pybel_formats, Obabel_formats

# List of supported converters.
BACKENDS = [
    Pybel_converter,
    Obabel_converter
]

FORMAT_BACKENDS = [
    Pybel_formats,
    Obabel_formats,
    formats
]

# Supported formats.
READ_FORMATS = formats().read()
WRITE_FORMATS = formats().write()

# Path to the data directory.
DATA = Path(__file__).parent / "data"