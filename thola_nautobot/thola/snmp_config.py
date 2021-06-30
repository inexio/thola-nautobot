"""SNMP config for thola nautobot."""
from thola_nautobot.models import TholaDevice
from django.conf import settings


PLUGIN_SETTINGS = settings.PLUGINS_CONFIG["thola_nautobot"]

class SNMPConfig:
    """Class that stores snmp config."""

    def __init__(self, community, version, port, discover_retries, discover_timeout, discover_par_requests):
        """Create an snmp config."""
        self.community = PLUGIN_SETTINGS["snmp_community"]
        self.version = PLUGIN_SETTINGS["snmp_version"]
        self.port = PLUGIN_SETTINGS["snmp_port"]
        self.discover_retries = PLUGIN_SETTINGS["snmp_discover_retries"]
        self.discover_timeout = PLUGIN_SETTINGS["snmp_discover_timeout"]
        self.discover_par_requests = PLUGIN_SETTINGS["snmp_discover_par_requests"]
        if community is not None and community != "":
            self.community = community
        if version is not None and version != "":
            self.version = version
        if port is not None:
            self.port = port
        if discover_retries is not None:
            self.discover_retries = discover_retries
        if discover_timeout is not None:
            self.discover_timeout = discover_timeout
        if discover_par_requests is not None:
            self.discover_par_requests = discover_par_requests


def from_thola_device(thola_device: TholaDevice) -> SNMPConfig:
    """Returns a new instance of an snmp config."""

    return SNMPConfig(thola_device.snmp_community, thola_device.snmp_version, thola_device.snmp_port,
                      thola_device.snmp_discover_retries, thola_device.snmp_discover_timeout,
                      thola_device.snmp_discover_par_requests)
