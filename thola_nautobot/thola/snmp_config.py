"""SNMP config for thola nautobot."""
from thola_nautobot.models import TholaDevice


class SNMPConfig:
    """Class that stores snmp config."""

    def __init__(self, community, version, port, discover_retries, discover_timeout, discover_par_requests):
        """Create an snmp config."""
        self.community = "public"
        self.version = "2c"
        self.port = 161
        self.discover_retries = 0
        self.discover_timeout = 2
        self.discover_par_requests = 5
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
