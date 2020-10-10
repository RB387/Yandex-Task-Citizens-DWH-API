from abc import ABC


class AbstractClient(ABC):
    """
    Abstract client interface that should be used in app builder
    """

    NAME: str

    def __init__(self, *args, **kwargs):  # pylint: disable=unused-argument
        ...
