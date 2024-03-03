import importlib.metadata


def cli_main():
    print("DWB CLI...", "p=", __package__, "n=", __name__)
    __version__ = importlib.metadata.version("miro-dataworkbench")
    print("V:", __version__)
