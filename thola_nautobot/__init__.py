"""Plugin declaration for thola_nautobot."""

__version__ = '0.1.0'

from nautobot.extras.plugins import PluginConfig


class Thola(PluginConfig):
    """Plugin configuration for the thola_nautobot plugin."""

    name = 'thola_nautobot'
    verbose_name = 'Thola Nautobot'
    description = 'Thola plugin for Nautobot'
    version = __version__
    author = 'Thola Team'
    author_email = 'nautobot@thola.io'
    required_settings = []


config = Thola
