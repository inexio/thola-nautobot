"""SNMP config for thola nautobot."""


class SNMPConfig:
    """Class that stores snmp config."""

    def __init__(self, thola_device):
        """Create an snmp config."""
        self.community = "public"
        self.version = "2c"
        self.port = 161
        self.discover_retries = 0
        self.discover_timeout = 2
        self.discover_par_requests = 5
        if thola_device.snmp_community is not None and thola_device.snmp_community is not "":
            self.community = thola_device.snmp_community
        if thola_device.snmp_version is not None and thola_device.snmp_version is not "":
            self.version = thola_device.snmp_version
        if thola_device.snmp_port is not None:
            self.port = thola_device.snmp_port
        if thola_device.snmp_discover_retries is not None:
            self.discover_retries = thola_device.snmp_discover_retries
        if thola_device.snmp_discover_timeout is not None:
            self.discover_timeout = thola_device.snmp_discover_timeout
        if thola_device.snmp_discover_par_requests is not None:
            self.discover_par_requests = thola_device.snmp_discover_par_requests
