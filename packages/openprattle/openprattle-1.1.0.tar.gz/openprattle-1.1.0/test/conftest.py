import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--formats", action="store_true", default=False, help="run format conversion tests")


def pytest_configure(config):
    config.addinivalue_line("markers", "formats: mark a format conversion test")


def pytest_collection_modifyitems(config, items):
#     if config.getoption("--run-slow"):
#         # Asked to run slow tests, do nothing.
#         return
    

    skip = pytest.mark.skip(reason="need --formats option to run")
    for item in items:
        if "formats" in item.keywords and not config.getoption("--formats"):
            item.add_marker(skip)
