"""Plugin declaration for thola nautobot."""

__version__ = '0.2.0'

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
        'snmp_community': 'public',
        'snmp_version': '2c',
        'snmp_port': 161,
        'snmp_discover_par_requests': 5,
        'snmp_discover_timeout': 2,
        'snmp_discover_retries': 0,
        'onboarding_create_models': True,
        'onboarding_device_name': True
    }


config = Thola
