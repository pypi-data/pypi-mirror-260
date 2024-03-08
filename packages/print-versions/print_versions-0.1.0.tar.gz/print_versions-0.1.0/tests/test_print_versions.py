from print_versions import __version__, get_versions, print_versions


def test_get_versions():
    expected = {"print_versions": __version__}
    res = get_versions(globals(), skip=None)
    assert res == expected


def test_print_versions(capsys):
    expected = f"print_versions=={__version__}\n"
    print_versions(globals(), skip=None)
    captured = capsys.readouterr()
    assert captured.out == expected
