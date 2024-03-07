import os
import re

from io import StringIO
from pathlib import Path
from shutil import rmtree
from unittest.mock import patch, mock_open

import pytest
import unittest

from eumdac.cli import cli
from .base import INTEGRATION_TESTING


@pytest.fixture
@unittest.skipIf(INTEGRATION_TESTING, "Covered by integration testing")
def temp_output_dir(request):
    output_dir_name = f"output_dir_{request.node.name}"
    yield Path(output_dir_name)
    rmtree(output_dir_name)


@pytest.fixture
@unittest.skipIf(INTEGRATION_TESTING, "Covered by integration testing")
def temp_config_dir(request):
    config_dir_name = Path(f"config_dir_{request.node.name}")
    os.environ["EUMDAC_CONFIG_DIR"] = str(config_dir_name)
    config_dir_name.mkdir()

    yield config_dir_name
    rmtree(config_dir_name)
    del os.environ["EUMDAC_CONFIG_DIR"]


@pytest.fixture
@unittest.skipIf(INTEGRATION_TESTING, "Covered by integration testing")
def temp_credentials(temp_config_dir):
    credentials_path = temp_config_dir / "credentials"
    with credentials_path.open("w") as fobj:
        fobj.write("user,password")
    yield credentials_path


def eumdac(args):
    test_out = StringIO()
    test_err = StringIO()

    with patch("sys.stdout", test_out), patch("sys.stderr", test_err), patch(
        "eumdac.cli.sys.stdin", new_callable=mock_open()
    ) as mock_stdin:
        mock_stdin.isatty.return_value = False
        try:
            cli(args)
        except SystemExit as exc:
            if exc.code != 0:
                raise exc

    return test_out.getvalue(), test_err.getvalue()


def assert_eumdac_output(args, regex):
    out, err = eumdac(args)

    print(out)
    mat = re.search(regex, out)

    assert mat, (
        f"Output of \neumdac {' '.join(args)}\n"
        "did not match.\n"
        "---\n"
        f"The regex was '{regex}'\n"
        "---\n"
        "The output was:\n"
        "---\n"
        f"{out}"
        "---\n"
    )
    assert not err, "stderr not empty!\n" "Contents:\n" f"{err}"


@unittest.skipIf(INTEGRATION_TESTING, "Covered by integration testing")
def test_set_credentials(temp_config_dir):
    args = "--set-credentials user password".split()
    regex = (
        r"Credentials are correct. Token was generated.*\n"
        r"Credentials are written to file .*credentials"
    )
    with patch("eumdac.token.AccessToken._update_token_data"):
        assert_eumdac_output(args, regex)


@unittest.skipIf(INTEGRATION_TESTING, "Covered by integration testing")
def test_download_product(temp_credentials, temp_output_dir):
    args = f"download -c MockCollection -p MockProduct -o {temp_output_dir} --test".split()
    regex = r".*Downloading.*MockProduct.*\r?\n"
    assert_eumdac_output(args, regex)


@unittest.skipIf(INTEGRATION_TESTING, "Covered by integration testing")
def test_skip_download_product(temp_credentials, temp_output_dir):
    args = f"download -c MockCollection -p MockProduct -o {temp_output_dir} --test".split()
    regex = r"Skip .* already exists"

    # First run to ensure the file exists already
    eumdac(args)
    assert_eumdac_output(args, regex)


@unittest.skipIf(INTEGRATION_TESTING, "Covered by integration testing")
def test_download_product_entry(temp_credentials, temp_output_dir):
    args = f"download -c MockCollection -p MockProduct --entry *.nc -o {temp_output_dir} --test".split()
    # we expect a folder with the product name to be created when --entry is given
    regex = r".*Downloading.*MockProduct.*MockProduct.*\r?\n"
    assert_eumdac_output(args, regex)


@unittest.skipIf(INTEGRATION_TESTING, "Covered by integration testing")
def test_download_output_dir(temp_credentials, temp_output_dir):
    args = f"download -c MockCollection --time-range 2020-03-01 2020-03-01T12:15 -o {temp_output_dir} --test".split()
    regex = rf"Output directory: .*?{temp_output_dir}.*\r?\n(.*Downloading.*\r?\n).*\r?\n"
    assert_eumdac_output(args, regex)
