import json
import subprocess


def test_bash_kernel_registered():
    out = subprocess.run(
        ["jupyter", "kernelspec", "list", "--json"],
        capture_output=True, text=True, check=True,
    )
    specs = json.loads(out.stdout)["kernelspecs"]
    assert "bash" in specs, f"kernels found: {sorted(specs)}"


def test_python3_kernel_registered():
    out = subprocess.run(
        ["jupyter", "kernelspec", "list", "--json"],
        capture_output=True, text=True, check=True,
    )
    assert "python3" in json.loads(out.stdout)["kernelspecs"]


def test_server_extensions_load_without_error():
    out = subprocess.run(
        ["jupyter", "server", "extension", "list"],
        capture_output=True, text=True,
    )
    # jupyter writes this listing to stderr
    combined = out.stdout + out.stderr
    assert "jupyter_resource_usage" in combined, combined
    assert "Error loading" not in combined, combined