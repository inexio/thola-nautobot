"""Utilities for thola nautobot."""
import re


def normalize_ipv4(ip):
    """
    Remove the network mask from the ip address.
    e.g. 0.0.0.0/24 -> 0.0.0.0
    """

    regex = r'(\d+)[.](\d+)[.](\d+)[.](\d+)[/](\d+)'
    if not re.findall(regex, ip):
        return ip

    p = re.split(regex, ip)
    return "%s.%s.%s.%s" % (p[1], p[2], p[3], p[4])
