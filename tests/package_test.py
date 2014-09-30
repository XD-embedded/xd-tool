def test_version():
    import xd.tool
    assert isinstance(xd.tool.__version__, str)
    assert xd.tool.__version__ == "0.1.0"
