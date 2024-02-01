from many.utils import resolve_kwargs


def test_resolve_kwargs():
    assert resolve_kwargs(["--some_kwarg_up", "Some value"]) == {
        "some_kwarg_up": "Some value"
    }
