from . import available


def test_available():
    assert len(available) > 0


def test_entries():
    for value in available.values():
        assert len(value.examples) > 0
