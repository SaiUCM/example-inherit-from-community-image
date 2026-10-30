"""
Version pins that other packages depend on.
Testing that these versions are compatible with the current environment.
"""

import pytest


def test_numpy_importable():
    import numpy
    assert numpy.__version__, f"numpy not importable, version={numpy.__version__}"


def test_python_is_3x():
    import sys
    assert sys.version_info[0] == 3 and sys.version_info[1] >= 11, (
        f"Expected Python 3.11+, got {sys.version}"
    )


def test_ipywidgets_is_v8():
    import ipywidgets
    assert ipywidgets.__version__.startswith("8."), ipywidgets.__version__


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