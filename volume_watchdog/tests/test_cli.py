from volume_watchdog import cli


def test_cli():
    assert cli.main(None, False) is None
