"""Test loadtext."""
from loadtext import loadtext

def test_default():
    """Test default."""
    assert len(loadtext("loadtext/__init__.py")) > 100

def test_splitlines():
    """Test splitliens=True."""
    assert len(loadtext("loadtext/__init__.py", True)) >= 5
