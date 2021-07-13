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


def is_ipv4(ip):
    """Checks if the ip address is a valid ipv4 address including CIDR mask."""

    regex = r'^(\d+)[.](\d+)[.](\d+)[.](\d+)[/](\d+)$'
    pattern = re.compile(regex)
    return pattern.search(ip) is not None


def get_prefixlength(ip):
    """Returns the length of the network prefix, in bits."""

    regex = r'(\d+)[.](\d+)[.](\d+)[.](\d+)[/](\d+)'
    if not re.findall(regex, ip):
        return ip

    p = re.split(regex, ip)
    return int(p[5])
