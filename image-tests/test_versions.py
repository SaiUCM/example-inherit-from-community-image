"""
Version pins that other packages depend on.
Testing that these versions are compatible with the current environment.
"""

import pytest


def test_numpy_is_v1():
    import numpy
    assert numpy.__version__.startswith("1."), (
        f"environment.yml pins numpy<2, got {numpy.__version__}. "
        "See commit 5b8dcff: pip pulling numpy 2.x breaks otter-grader "
        "and pyarmor. Check whether a pip dependency is overriding conda."
    )


def test_python_is_311():
    import sys
    assert sys.version_info[:2] == (3, 11), sys.version


def test_ipywidgets_is_v8():
    import ipywidgets
    assert ipywidgets.__version__.startswith("8."), ipywidgets.__version__


@pytest.mark.xfail(
    reason="kaleido 1.0.0 vs plotly 5.19 — fig.write_image() is broken in the "
           "image today. Pin python-kaleido=0.2.1 or bump plotly>=6.1.1. See #N.",
    strict=True,
)
def test_kaleido_plotly_compatible():
    from importlib.metadata import version
    import plotly

    kaleido_version = version("kaleido")
    k_major = int(kaleido_version.split(".")[0])
    p_major = int(plotly.__version__.split(".")[0])
    assert (k_major >= 1) == (p_major >= 6), (
        f"kaleido {kaleido_version} / plotly {plotly.__version__} are "
        "incompatible — fig.write_image() silently fails. kaleido 1.x needs "
        "plotly>=6.1.1; plotly 5.x needs kaleido 0.2.1."
    )