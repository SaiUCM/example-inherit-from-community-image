# image-tests/test_otter.py
"""
otter-grader coverage.

otter is what faculty use to autograde student work, so a broken otter
is a broken semester. `import otter` alone proves almost nothing — these
tests walk from the version pin up to a real grading run.
"""

import json
import subprocess
import textwrap

import pytest


def test_otter_version_pinned():
    """environment.yml pins otter-grader==6.1.3."""
    import otter
    assert otter.__version__.startswith("6.1"), otter.__version__


def test_otter_cli_available():
    """Instructors invoke `otter assign` / `otter generate` from a terminal,
    not from Python. The console script has to be on PATH."""
    out = subprocess.run(["otter", "--version"], capture_output=True, text=True)
    assert out.returncode == 0, out.stderr


def test_otter_extras_importable():
    """environment.yml requests otter-grader[grading,plugins]; the extras
    pull separate dependency trees that can resolve badly on their own."""
    import otter.assign
    import otter.generate


def test_student_notebook_api():
    """The student-facing surface: every assignment notebook opens with
    `otter.Notebook()` and calls `.check()` on it."""
    import otter
    assert hasattr(otter, "Notebook")


def test_otter_check_passes_and_fails(tmp_path):
    """A real grading round-trip: a correct answer must pass and a wrong
    answer must fail. A grader that always passes is worse than none."""
    test_dir = tmp_path / "tests"
    test_dir.mkdir()
    (test_dir / "q1.py").write_text(textwrap.dedent("""
        OK_FORMAT = True
        test = {
            "name": "q1",
            "points": 1,
            "suites": [{
                "cases": [{"code": ">>> answer\\n42"}],
                "type": "doctest",
            }],
        }
    """))

    import otter
    grader = otter.Notebook(tests_dir=str(test_dir))

    answer = 42
    assert grader.check("q1", global_env={"answer": answer}).grade == 1

    answer = 41
    assert grader.check("q1", global_env={"answer": answer}).grade == 0