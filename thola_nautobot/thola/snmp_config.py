"""SNMP config for thola nautobot."""


class SNMPConfig:
    """Class that stores snmp config."""

    def __init__(self, community, version, port, discover_par_request, discover_retries, discover_timeout):
        """Create an snmp config."""
        self.community = community
        self.version = version
        self.port = port
        self.discover_par_request = discover_par_request
        self.discover_retries = discover_retries
        self.discover_timeout = discover_timeout
