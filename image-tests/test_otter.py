"""
Comprehensive otter-grader tests.
Covers: module imports, all CLI commands, otter assign workflow,
        otter export API, otter generate, otter grade API, plugins, check API.
"""

import json
import subprocess
from pathlib import Path
import pytest


# ── Notebook fixtures ─────────────────────────────────────────────────────────

# Master notebook in otter-assign format (raw cells for config/question blocks)
MASTER_NB = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11.8"}
    },
    "cells": [
        {
            "cell_type": "raw",
            "id": "config",
            "metadata": {},
            "source": "# ASSIGNMENT CONFIG\nname: test_hw\n"
        },
        {
            "cell_type": "markdown",
            "id": "intro",
            "metadata": {},
            "source": "# Test Assignment\n"
        },
        {
            "cell_type": "raw",
            "id": "q1",
            "metadata": {},
            "source": "# BEGIN QUESTION\nname: q1\npoints: 1\n"
        },
        {
            "cell_type": "markdown",
            "id": "q1-prompt",
            "metadata": {},
            "source": "**Q1:** Set `x` to 5.\n"
        },
        {
            "cell_type": "code",
            "id": "q1-solution",
            "metadata": {},
            "outputs": [],
            "source": "# BEGIN SOLUTION\nx = 5\n# END SOLUTION\n"
        },
        {
            "cell_type": "code",
            "id": "q1-public-tests",
            "metadata": {},
            "outputs": [],
            "source": "# BEGIN TESTS\nassert x == 5\n# END TESTS\n"
        },
        {
            "cell_type": "code",
            "id": "q1-hidden-tests",
            "metadata": {},
            "outputs": [],
            "source": "# BEGIN HIDDEN TESTS\nassert isinstance(x, int)\n# END HIDDEN TESTS\n"
        }
    ]
}

SIMPLE_NB = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11.8"}
    },
    "cells": [
        {
            "cell_type": "markdown",
            "id": "title",
            "metadata": {},
            "source": "# Simple Notebook\n"
        },
        {
            "cell_type": "code",
            "id": "code1",
            "metadata": {},
            "outputs": [{"output_type": "stream", "name": "stdout", "text": "2\n"}],
            "source": "x = 1 + 1\nprint(x)\n"
        }
    ]
}


@pytest.fixture
def master_nb(tmp_path):
    p = tmp_path / "master.ipynb"
    p.write_text(json.dumps(MASTER_NB))
    return p


@pytest.fixture
def simple_nb(tmp_path):
    p = tmp_path / "notebook.ipynb"
    p.write_text(json.dumps(SIMPLE_NB))
    return p


def otter_cmd(*args):
    return subprocess.run(["otter", *args], capture_output=True, text=True)


# ── Module imports ────────────────────────────────────────────────────────────

def test_otter_import():
    import otter
    assert otter is not None

def test_otter_version_attr():
    import otter
    assert otter.__version__ == "6.1.3"

def test_otter_assign_module():
    import otter.assign
    assert otter.assign is not None

def test_otter_assign_main_callable():
    from otter.assign import main
    assert callable(main)

def test_otter_grade_module():
    import otter.grade
    assert otter.grade is not None

def test_otter_grade_main_callable():
    from otter.grade import main
    assert callable(main)

def test_otter_export_module():
    import otter.export
    assert otter.export is not None

def test_otter_export_notebook_callable():
    from otter.export import export_notebook
    assert callable(export_notebook)

def test_otter_check_module():
    import otter.check
    assert otter.check is not None

def test_otter_check_notebook_class():
    from otter.check.notebook import Notebook
    assert Notebook is not None

def test_otter_plugins_module():
    import otter.plugins
    assert otter.plugins is not None

def test_otter_plugins_collection_class():
    from otter.plugins import PluginCollection
    assert PluginCollection is not None

def test_otter_generate_module():
    import otter.generate
    assert otter.generate is not None

def test_otter_generate_main_callable():
    from otter.generate import main
    assert callable(main)

def test_otter_run_module():
    import otter.run
    assert otter.run is not None

def test_otter_utils_module():
    import otter.utils
    assert otter.utils is not None


# ── CLI: version and all subcommands ─────────────────────────────────────────

def test_cli_version():
    r = otter_cmd("--version")
    assert r.returncode == 0
    assert "6.1.3" in r.stdout

def test_cli_help_lists_all_commands():
    r = otter_cmd("--help")
    assert r.returncode == 0
    for cmd in ["assign", "check", "export", "generate", "grade", "run"]:
        assert cmd in r.stdout, f"'{cmd}' missing from otter --help"

def test_cli_assign_help():
    r = otter_cmd("assign", "--help")
    assert r.returncode == 0
    assert "MASTER" in r.stdout
    assert "RESULT" in r.stdout

def test_cli_grade_help():
    r = otter_cmd("grade", "--help")
    assert r.returncode == 0
    assert "autograder" in r.stdout

def test_cli_export_help():
    r = otter_cmd("export", "--help")
    assert r.returncode == 0
    assert "SRC" in r.stdout

def test_cli_generate_help():
    r = otter_cmd("generate", "--help")
    assert r.returncode == 0
    assert "zip" in r.stdout

def test_cli_run_help():
    r = otter_cmd("run", "--help")
    assert r.returncode == 0
    assert "SUBMISSION" in r.stdout

def test_cli_check_help():
    r = otter_cmd("check", "--help")
    assert r.returncode == 0


# ── otter assign ──────────────────────────────────────────────────────────────

def test_assign_exits_successfully(tmp_path, master_nb):
    out = tmp_path / "dist"
    r = otter_cmd("assign", "--no-run-tests", "--no-pdfs", str(master_nb), str(out))
    assert r.returncode == 0, f"otter assign failed\nstdout: {r.stdout}\nstderr: {r.stderr}"

def test_assign_creates_student_directory(tmp_path, master_nb):
    out = tmp_path / "dist"
    otter_cmd("assign", "--no-run-tests", "--no-pdfs", str(master_nb), str(out))
    assert (out / "student").is_dir()

def test_assign_creates_autograder_directory(tmp_path, master_nb):
    out = tmp_path / "dist"
    otter_cmd("assign", "--no-run-tests", "--no-pdfs", str(master_nb), str(out))
    assert (out / "autograder").is_dir()

def test_assign_student_notebook_exists(tmp_path, master_nb):
    out = tmp_path / "dist"
    otter_cmd("assign", "--no-run-tests", "--no-pdfs", str(master_nb), str(out))
    assert (out / "student" / "master.ipynb").exists()

def test_assign_autograder_notebook_exists(tmp_path, master_nb):
    out = tmp_path / "dist"
    otter_cmd("assign", "--no-run-tests", "--no-pdfs", str(master_nb), str(out))
    assert (out / "autograder" / "master.ipynb").exists()

def test_assign_student_has_otter_init_cell(tmp_path, master_nb):
    # otter assign injects an initialization cell as the very first code cell
    out = tmp_path / "dist"
    otter_cmd("assign", "--no-run-tests", "--no-pdfs", str(master_nb), str(out))
    nb = json.loads((out / "student" / "master.ipynb").read_text())
    first_code = next(c for c in nb["cells"] if c["cell_type"] == "code")
    src = "".join(first_code["source"]) if isinstance(first_code["source"], list) else first_code["source"]
    assert "import otter" in src
    assert "otter.Notebook" in src

def test_assign_student_notebook_is_valid_json(tmp_path, master_nb):
    out = tmp_path / "dist"
    otter_cmd("assign", "--no-run-tests", "--no-pdfs", str(master_nb), str(out))
    nb = json.loads((out / "student" / "master.ipynb").read_text())
    assert nb["nbformat"] == 4

def test_assign_autograder_notebook_is_valid_json(tmp_path, master_nb):
    out = tmp_path / "dist"
    otter_cmd("assign", "--no-run-tests", "--no-pdfs", str(master_nb), str(out))
    nb = json.loads((out / "autograder" / "master.ipynb").read_text())
    assert nb["nbformat"] == 4

def test_assign_student_notebook_has_cells(tmp_path, master_nb):
    out = tmp_path / "dist"
    otter_cmd("assign", "--no-run-tests", "--no-pdfs", str(master_nb), str(out))
    nb = json.loads((out / "student" / "master.ipynb").read_text())
    assert len(nb["cells"]) > 0

def test_assign_autograder_has_tests_preserved(tmp_path, master_nb):
    out = tmp_path / "dist"
    otter_cmd("assign", "--no-run-tests", "--no-pdfs", str(master_nb), str(out))
    content = (out / "autograder" / "master.ipynb").read_text()
    assert "assert x == 5" in content

def test_assign_student_has_export_cell(tmp_path, master_nb):
    # otter assign injects a final export cell so students can submit their work
    out = tmp_path / "dist"
    otter_cmd("assign", "--no-run-tests", "--no-pdfs", str(master_nb), str(out))
    nb = json.loads((out / "student" / "master.ipynb").read_text())
    code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    last_src = "".join(code_cells[-1]["source"]) if isinstance(code_cells[-1]["source"], list) else code_cells[-1]["source"]
    assert "grader.export" in last_src


# ── otter export ─────────────────────────────────────────────────────────────

def test_export_api_is_importable():
    from otter.export import export_notebook
    assert callable(export_notebook)

def test_export_cli_help_shows_exporter_options():
    r = otter_cmd("export", "--help")
    assert "latex" in r.stdout
    assert "html" in r.stdout

def test_export_cli_help_shows_filtering_option():
    r = otter_cmd("export", "--help")
    assert "filtering" in r.stdout

def test_export_cli_help_shows_save_option():
    r = otter_cmd("export", "--help")
    assert "--save" in r.stdout


# ── otter generate ────────────────────────────────────────────────────────────

def test_generate_creates_zip(tmp_path):
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    out_zip = tmp_path / "autograder.zip"
    r = otter_cmd("generate", "--tests-dir", str(tests_dir), "--output-path", str(out_zip))
    assert r.returncode == 0, f"otter generate failed\nstdout: {r.stdout}\nstderr: {r.stderr}"
    assert out_zip.exists()

def test_generate_zip_is_nonempty(tmp_path):
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    out_zip = tmp_path / "autograder.zip"
    otter_cmd("generate", "--tests-dir", str(tests_dir), "--output-path", str(out_zip))
    assert out_zip.stat().st_size > 0


# ── otter grade API ───────────────────────────────────────────────────────────

def test_grade_main_is_callable():
    from otter.grade import main
    assert callable(main)


# ── otter plugins ─────────────────────────────────────────────────────────────

def test_plugin_collection_instantiable():
    from otter.plugins import PluginCollection
    # Empty plugin list, no submission — just verifies the class initialises
    pc = PluginCollection([], "", {})
    assert pc is not None

def test_plugin_collection_with_empty_plugins():
    from otter.plugins import PluginCollection
    pc = PluginCollection([], "", {})
    assert len(pc._plugins) == 0


# ── otter check API ───────────────────────────────────────────────────────────

def test_check_notebook_class_importable():
    from otter.check.notebook import Notebook
    assert Notebook is not None

def test_check_notebook_has_check_method():
    from otter.check.notebook import Notebook
    assert hasattr(Notebook, "check")

def test_check_notebook_has_export_method():
    from otter.check.notebook import Notebook
    assert hasattr(Notebook, "export")
