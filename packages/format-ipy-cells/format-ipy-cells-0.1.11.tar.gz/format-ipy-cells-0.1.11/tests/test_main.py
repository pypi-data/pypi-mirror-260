import difflib
import filecmp
import shutil
from importlib.metadata import version
from pathlib import Path

import pytest

from format_ipy_cells.main import main


def test_main_format_cells(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    shutil.copy2("tests/fixtures/raw_nb.py", raw_tmp := str(tmp_path / "raw_nb.py"))
    # test we leave clean file as is and don't print logs about it
    clean_nb = "tests/fixtures/clean_nb.py"
    shutil.copy2(clean_nb, clean_tmp := str(tmp_path / "clean_nb.py"))

    ret = main((raw_tmp, clean_tmp))
    assert ret == 1

    with open(clean_nb) as file, open(clean_tmp) as tmp_file:
        clean_lines, tmp_lines = file.readlines(), tmp_file.readlines()
    file_diff = "\n".join(difflib.unified_diff(clean_lines, tmp_lines))

    assert filecmp.cmp(
        raw_tmp, clean_nb, shallow=False
    ), f"Formatted file has unexpected content:\n{file_diff}"
    assert filecmp.cmp(
        clean_tmp, clean_nb, shallow=False
    ), "clean file should not have changed"

    out, err = capsys.readouterr()
    assert out == f"Rewriting {raw_tmp}\n"
    assert err == ""

    ret = main([clean_tmp])
    assert ret == 0, "expected exit code 0 when no files were changed"
    out, err = capsys.readouterr()
    assert out == err == ""


def test_main_print_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit, match="^0$"):
        main(["-v"])

    stdout, stderr = capsys.readouterr()

    fic_version = version("format-ipy-cells")

    assert stdout == f"format-ipy-cells v{fic_version}\n"
    assert stderr == ""
