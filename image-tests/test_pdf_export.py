import os
import pathlib
import subprocess

import nbformat


def test_chromium_present():
    """Fast check — fails in ms instead of waiting on the export below."""
    root = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    assert root, (
        "PLAYWRIGHT_BROWSERS_PATH is unset. Browsers would land in "
        "~/.cache/ms-playwright, which the hub's persistent home volume "
        "mounts over at runtime."
    )
    root = pathlib.Path(root)
    assert root.is_dir(), f"{root} missing"
    assert any(root.glob("chromium-*")), f"no chromium in {list(root.iterdir())}"


def test_webpdf_export(tmp_path):
    nb = nbformat.v4.new_notebook(
        cells=[nbformat.v4.new_code_cell("print('hello')")]
    )
    src = tmp_path / "sample.ipynb"
    nbformat.write(nb, str(src))

    result = subprocess.run(
        ["jupyter", "nbconvert", "--to", "webpdf", str(src)],
        capture_output=True, text=True, timeout=300,
    )
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "sample.pdf").stat().st_size > 0


def test_torchvision_compiled_ops():
    """Exercises the C++ extension, not just the Python shim — this is
    what breaks when torch and torchvision drift apart."""
    import torch
    from torchvision.ops import nms

    boxes = torch.tensor([[0., 0., 1., 1.], [0., 0., 1., 1.]])
    scores = torch.tensor([0.9, 0.8])
    assert len(nms(boxes, scores, 0.5)) == 1