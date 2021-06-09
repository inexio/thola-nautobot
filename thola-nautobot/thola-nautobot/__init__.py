from nautobot.extras.plugins import PluginConfig


class AnimalSoundsConfig(PluginConfig):
    name = 'thola-nautobot'
    verbose_name = 'Thola Nautobot'
    description = 'Thola plugin for Nautobot'
    version = '0.1.0'
    author = 'Thola Team'
    author_email = 'nautobot@thola.io'
    required_settings = []
    default_settings = {
        'loud': False
    }


config = AnimalSoundsConfig
