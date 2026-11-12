"""Minimal CPU smoke test.

Verifies only that the package imports and that PyTorch is available
in the environment. It does NOT load any model, download weights, or
run inference.
"""

import torch

import evermind


def test_package_imports() -> None:
    assert evermind.__version__ == "0.1.0"


def test_torch_available() -> None:
    assert torch.__version__
    # CPU-only smoke check: creating a tiny tensor must work without a GPU.
    assert torch.tensor([1.0, 2.0]).sum().item() == 3.0
