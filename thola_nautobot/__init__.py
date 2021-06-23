"""Plugin declaration for thola nautobot."""

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
    default_settings = {
        'thola_api': 'http://localhost:8237',
        'snmp_defaults': {
            'community': 'public',
            'version': '2c',
            'port': 161,
            'discover_par_requests': 5,
            'discover_timeout': 2,
            'discover_retries': 0
        }
    }


config = Thola
