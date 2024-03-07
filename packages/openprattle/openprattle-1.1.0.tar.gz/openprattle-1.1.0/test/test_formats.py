"""Test the supported formats."""

import pytest
from pathlib import Path

from test import DATA, BACKENDS, WRITE_FORMATS, READ_FORMATS

@pytest.mark.formats
@pytest.mark.parametrize("backend", BACKENDS)
@pytest.mark.parametrize("write_format", WRITE_FORMATS)
def test_out_formats(backend, write_format, tmp_path):
    """
    """
    converter = backend(input_file_path = Path(DATA, "Benzene.cml"), input_file_type = "cml")

    converter.convert(write_format, Path(tmp_path, Path("Benzene").with_suffix("." + write_format)))

@pytest.mark.formats
@pytest.mark.parametrize("backend", BACKENDS)
@pytest.mark.parametrize("read_format", READ_FORMATS)
def test_in_formats(backend, read_format, tmp_path):
    """
    """
    input_file_path = Path(DATA, Path("Benzene").with_suffix("." + read_format))

    if not input_file_path.exists():
        pytest.skip("No '{}' file available to test".format(input_file_path))

    converter = backend(input_file_path = input_file_path, input_file_type = read_format)

    converter.convert("cml", Path(tmp_path, "Benzene.cml"))


