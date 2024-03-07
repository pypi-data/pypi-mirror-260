"""Test the OpenPrattle library."""

import pytest

from pathlib import Path
import copy

from openprattle import Openbabel_converter

from test import DATA, BACKENDS, FORMAT_BACKENDS

BACKENDS = copy.copy(BACKENDS)
BACKENDS.append(Openbabel_converter.get_cls("cml"))


@pytest.mark.parametrize("backend", BACKENDS)
def test_conversion(backend, tmp_path):
    """Test simple file conversion."""

    converter = backend(input_file_path = Path(DATA, "Benzene.cml"), input_file_type = "cml")
    converter.convert("xyz", Path(tmp_path, "Benzene.xyz"))

@pytest.mark.parametrize("input_file_type", [
    "cml",
    "xyz",
    "cdx"
])
def test_auto_backend(input_file_type, tmp_path):
    """Test the ability to automatically pick an appropriate converter class."""
    converter = Openbabel_converter.from_file(input_file_path = Path(DATA, "Benzene." + input_file_type))
    converter.convert("xyz", Path(tmp_path, "Benzene.xyz"))

@pytest.mark.parametrize("formatter", FORMAT_BACKENDS)
@pytest.mark.parametrize("readwrite", ("read", "write"))
def test_available_read_formats(formatter, readwrite):
    """Test the ability to print supported input/output formats."""
    getattr(formatter(), readwrite)()
