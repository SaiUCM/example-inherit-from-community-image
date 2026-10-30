import pytest


# ── Core scientific stack ──────────────────────────────────────────────────────

def test_numpy():
    import numpy as np
    arr = np.array([1, 2, 3])
    assert arr.sum() == 6

def test_pandas():
    import pandas as pd
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    assert list(df.columns) == ["a", "b"]

def test_scipy():
    from scipy import stats
    assert stats.norm.pdf(0) > 0

def test_sklearn():
    from sklearn.linear_model import LinearRegression
    assert LinearRegression() is not None


# ── Visualization ──────────────────────────────────────────────────────────────

def test_plotly():
    import plotly.express as px
    fig = px.scatter(x=[1, 2], y=[3, 4])
    assert fig is not None

def test_kaleido():
    import importlib.metadata
    version = importlib.metadata.version("kaleido")
    assert version is not None

def test_ipyvuetify():
    import ipyvuetify
    assert ipyvuetify.__version__ is not None

def test_ipywidgets():
    import ipywidgets
    assert ipywidgets.__version__ is not None


# ── PyTorch (CPU build) ────────────────────────────────────────────────────────

def test_pytorch_import():
    import torch
    assert torch.__version__ is not None

def test_pytorch_cpu_tensor():
    import torch
    t = torch.tensor([1.0, 2.0, 3.0])
    assert t.sum().item() == 6.0

def test_pytorch_cpu_only():
    import torch
    # On linux-aarch64 (ARM), pytorch is always CPU-only — no CUDA support on this arch
    assert not torch.cuda.is_available()

def test_torchvision():
    import torchvision
    assert torchvision.__version__ is not None


# ── Sentence Transformers ──────────────────────────────────────────────────────

def test_sentence_transformers_import():
    from sentence_transformers import SentenceTransformer
    assert SentenceTransformer is not None


# ── Jupyter / notebook tooling ─────────────────────────────────────────────────

def test_nbgitpuller():
    import nbgitpuller
    assert nbgitpuller.__version__ is not None

def test_jupyter_resource_usage():
    import jupyter_resource_usage
    assert jupyter_resource_usage is not None

def test_bash_kernel():
    import bash_kernel
    assert bash_kernel is not None

def test_solara():
    import solara
    assert solara.__version__ is not None


# ── Course-specific packages ───────────────────────────────────────────────────

def test_datascience():
    from datascience import Table
    t = Table().with_columns("x", [1, 2, 3])
    assert t.num_rows == 3

def test_babypandas():
    import babypandas as bpd
    df = bpd.DataFrame().assign(x=[1, 2, 3])
    assert df.shape[0] == 3

def test_ISLP():
    import ISLP
    assert ISLP is not None

def test_astroML():
    import astroML
    assert astroML is not None


# ── Otter-grader ───────────────────────────────────────────────────────────────

def test_otter_import():
    import otter
    assert otter is not None

def test_otter_version():
    import otter
    assert otter.__version__ == "6.1.3"

def test_otter_grade_module():
    import otter.grade
    assert otter.grade is not None

def test_otter_plugins_module():
    import otter.plugins
    assert otter.plugins is not None

def test_otter_check_module():
    import otter.check
    assert otter.check is not None

def test_otter_export_module():
    import otter.export
    assert otter.export is not None

def test_otter_grading_extras():
    from otter.grade import main as grade_main
    assert callable(grade_main)


# ── nbconvert / PDF export ─────────────────────────────────────────────────────

def test_nbconvert():
    import nbconvert
    assert nbconvert.__version__ is not None

def test_nbconvert_webpdf_exporter():
    from nbconvert.exporters import WebPDFExporter
    assert WebPDFExporter is not None


# ── Playwright (browser automation for testing) ────────────────────────────────

def test_playwright_import():
    from playwright.sync_api import sync_playwright
    assert sync_playwright is not None
