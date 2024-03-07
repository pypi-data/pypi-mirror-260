from enum import Enum


class OutputFormat(str, Enum):
    """
    Output format for CLI commands.
    """

    default = 'default'
    json = 'json'
    wide = 'wide'
