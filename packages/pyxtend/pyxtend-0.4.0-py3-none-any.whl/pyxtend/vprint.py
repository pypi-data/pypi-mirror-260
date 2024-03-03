import contextlib


def vprint(*text: str) -> None:
    """
    Print the text if verbose=True in outer context.
    Print nothing if verbose=False or is undefined.
    """
    with contextlib.suppress(NameError):
        if verbose:
            print(*text)
