import hashlib


def create_hash(s: str):
    return hashlib.shake_256(s.encode()).hexdigest(5)


def resolve_kwargs(args):
    kwargs = dict()
    key = None
    for arg in args:
        if arg.startswith("--"):
            key = arg.removeprefix("--")
        elif key is not None:
            value = arg
            kwargs[key] = value
            key, value = None, None
    return kwargs
