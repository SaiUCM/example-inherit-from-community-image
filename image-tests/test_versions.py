"""
Version pins that other packages depend on
Testing that these versions are compatible with the current environment
"""

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
    