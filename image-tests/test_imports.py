import importlib
import pytest

PACKAGES = [
    "numpy",
    "pandas",
    "babypandas",
    "datascience",
    "plotly",
    "torch",
    "torchvision",
    # "sentence_transformers", broken package see #6
    "ipyvuetify",
    "ipywidgets",
    "otter",
    "solara",
    "ISLP",
    "astroML",
    "nbgitpuller",
    "nbconvert",
    "bash_kernel",
    "kaleido",
    "poppler",
    "jupyter_resource_usage",
]


@pytest.mark.parametrize("module", PACKAGES)
def test_import(module):
    importlib.import_module(module)