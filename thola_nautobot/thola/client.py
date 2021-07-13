"""Client methods for thola nautobot."""
import json

import urllib3
import sys
import thola_client
import thola_client.api.read_api as read
import thola_client.api.identify_api as identify
import thola_client.rest as rest
from django.conf import settings

import thola_nautobot.thola.snmp_config as sc
from thola_nautobot.thola.utils import normalize_ipv4

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG["thola_nautobot"]


def read_available_data(thola_config):
    """Reads data from the available components set on a given thola config."""
    snmp_config = sc.from_thola_config(thola_config)

    # check for correct snmp config
    wrong_config = "thola_nautobot config is incorrect | "
    wrong_variables = []
    if not isinstance(snmp_config.community, str):
        wrong_variables.append("snmp_config: Must be a string, ")
    if not isinstance(snmp_config.version, str):
        wrong_variables.append("snmp_version: Must be a string, ")
    if not isinstance(snmp_config.port, int):
        wrong_variables.append("snmp_port: Must be an integer, ")
    if not isinstance(snmp_config.discover_retries, int):
        wrong_variables.append("snmp_discover_retries: Must be an integer, ")
    if not isinstance(snmp_config.discover_timeout, int):
        wrong_variables.append("snmp_discover_timeout: Must be an integer, ")
    if not isinstance(snmp_config.discover_par_requests, int):
        wrong_variables.append("snmp_discover_par_requests: Must be an integer, ")

    # print incorrect snmp parameters
    if len(wrong_variables) != 0:
        for variable in wrong_variables:
            wrong_config += variable
        return {"error": wrong_config[0:len(wrong_config)-2]}

    host_ip = normalize_ipv4(str(thola_config.device.primary_ip4))
    api_host = PLUGIN_SETTINGS["thola_api"]
    results = {}
    stderr = sys.stderr
    sys.stderr = None  # disable stderr during execution
    try:
        if thola_config.cpu:
            results['cpu'] = thola_read_cpu_load(host_ip, snmp_config, api_host)
        if thola_config.disk:
            results['disk'] = thola_read_disk(host_ip, snmp_config, api_host)
        if thola_config.hardware_health:
            results['hardware_health'] = thola_read_hardware_health(host_ip, snmp_config, api_host)
        if thola_config.interfaces:
            results['interfaces'] = thola_read_interfaces(host_ip, snmp_config, api_host)
        if thola_config.memory:
            results['memory'] = thola_read_memory_usage(host_ip, snmp_config, api_host)
        if thola_config.server:
            results['server'] = thola_read_server(host_ip, snmp_config, api_host)
        if thola_config.ups:
            results['ups'] = thola_read_ups(host_ip, snmp_config, api_host)
    except urllib3.exceptions.MaxRetryError:
        sys.stderr = stderr  # enable stderr again
        return {"error": "Connection to Thola API couldn't be established"}
    sys.stderr = stderr  # enable stderr again
    return results


def thola_read_available_components(snmp_config, primary_ip):
    """Executes thola read available-components on a given device."""
    api_host = PLUGIN_SETTINGS["thola_api"]
    host_ip = normalize_ipv4(str(primary_ip))
    stderr = sys.stderr
    sys.stderr = None  # disable stderr during execution
    body = thola_client.ReadAvailableComponentsRequest(
        device_data=thola_client.DeviceData(
            ip_address=host_ip,
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[snmp_config.community],
                    versions=[snmp_config.version],
                    ports=[snmp_config.port],
                    discover_retries=snmp_config.discover_retries,
                    discover_timeout=snmp_config.discover_timeout,
                    discover_parallel_requests=snmp_config.discover_par_requests
                )
            )
        )
    )
    read_api = read.ReadApi()
    read_api.api_client.configuration.host = api_host
    try:
        result_dict = read_api.read_available_components(body=body).to_dict()
    except rest.ApiException as e:
        sys.stderr = stderr  # enable stderr again
        return json.loads(e.body)
    except urllib3.exceptions.MaxRetryError:
        sys.stderr = stderr  # enable stderr again
        return {"error": "Connection to Thola API couldn't be established"}
    sys.stderr = stderr  # enable stderr again
    return result_dict


def thola_read_cpu_load(host_ip, snmp_config, api_host):
    """Executes thola read cpu-load on a given device."""
    body = thola_client.ReadCPULoadRequest(
        device_data=thola_client.DeviceData(
            ip_address=host_ip,
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[snmp_config.community],
                    versions=[snmp_config.version],
                    ports=[snmp_config.port],
                    discover_retries=snmp_config.discover_retries,
                    discover_timeout=snmp_config.discover_timeout,
                    discover_parallel_requests=snmp_config.discover_par_requests
                )
            )
        )
    )
    read_api = read.ReadApi()
    read_api.api_client.configuration.host = api_host
    try:
        result_dict = read_api.read_cpu_load(body=body).to_dict()
    except rest.ApiException as e:
        return json.loads(e.body)
    except urllib3.exceptions.MaxRetryError as e:
        raise e
    return result_dict


def thola_read_disk(host_ip, snmp_config, api_host):
    """Executes thola read disk on a given device."""
    body = thola_client.ReadDiskRequest(
        device_data=thola_client.DeviceData(
            ip_address=host_ip,
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[snmp_config.community],
                    versions=[snmp_config.version],
                    ports=[snmp_config.port],
                    discover_retries=snmp_config.discover_retries,
                    discover_timeout=snmp_config.discover_timeout,
                    discover_parallel_requests=snmp_config.discover_par_requests
                )
            )
        )
    )
    read_api = read.ReadApi()
    read_api.api_client.configuration.host = api_host
    try:
        result_dict = read_api.read_disk(body=body).to_dict()
    except rest.ApiException as e:
        return json.loads(e.body)
    except urllib3.exceptions.MaxRetryError as e:
        raise e
    return result_dict


def thola_read_hardware_health(host_ip, snmp_config, api_host):
    """Executes thola read hardware-health on a given device."""
    body = thola_client.ReadHardwareHealthRequest(
        device_data=thola_client.DeviceData(
            ip_address=host_ip,
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[snmp_config.community],
                    versions=[snmp_config.version],
                    ports=[snmp_config.port],
                    discover_retries=snmp_config.discover_retries,
                    discover_timeout=snmp_config.discover_timeout,
                    discover_parallel_requests=snmp_config.discover_par_requests
                )
            )
        )
    )
    read_api = read.ReadApi()
    read_api.api_client.configuration.host = api_host
    try:
        result_dict = read_api.hardware_health(body=body).to_dict()
    except rest.ApiException as e:
        return json.loads(e.body)
    except urllib3.exceptions.MaxRetryError as e:
        raise e
    return result_dict


def thola_read_interfaces(host_ip, snmp_config, api_host):
    """Executes thola read interfaces on a given device."""
    body = thola_client.ReadInterfacesRequest(
        device_data=thola_client.DeviceData(
            ip_address=host_ip,
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[snmp_config.community],
                    versions=[snmp_config.version],
                    ports=[snmp_config.port],
                    discover_retries=snmp_config.discover_retries,
                    discover_timeout=snmp_config.discover_timeout,
                    discover_parallel_requests=snmp_config.discover_par_requests
                )
            )
        )
    )
    read_api = read.ReadApi()
    read_api.api_client.configuration.host = api_host
    try:
        result_dict = read_api.read_interfaces(body=body).to_dict()
    except rest.ApiException as e:
        return json.loads(e.body)
    except urllib3.exceptions.MaxRetryError as e:
        raise e
    return result_dict


def thola_read_memory_usage(host_ip, snmp_config, api_host):
    """Executes thola read memory-usage on a given device."""
    body = thola_client.ReadMemoryUsageRequest(
        device_data=thola_client.DeviceData(
            ip_address=host_ip,
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[snmp_config.community],
                    versions=[snmp_config.version],
                    ports=[snmp_config.port],
                    discover_retries=snmp_config.discover_retries,
                    discover_timeout=snmp_config.discover_timeout,
                    discover_parallel_requests=snmp_config.discover_par_requests
                )
            )
        )
    )
    read_api = read.ReadApi()
    read_api.api_client.configuration.host = api_host
    try:
        result_dict = read_api.read_memory_usage(body=body).to_dict()
    except rest.ApiException as e:
        return json.loads(e.body)
    except urllib3.exceptions.MaxRetryError as e:
        raise e
    return result_dict


def thola_read_server(host_ip, snmp_config, api_host):
    """Executes thola read server on a given device."""
    body = thola_client.ReadServerRequest(
        device_data=thola_client.DeviceData(
            ip_address=host_ip,
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[snmp_config.community],
                    versions=[snmp_config.version],
                    ports=[snmp_config.port],
                    discover_retries=snmp_config.discover_retries,
                    discover_timeout=snmp_config.discover_timeout,
                    discover_parallel_requests=snmp_config.discover_par_requests
                )
            )
        )
    )
    read_api = read.ReadApi()
    read_api.api_client.configuration.host = api_host
    try:
        result_dict = read_api.read_server(body=body).to_dict()
    except rest.ApiException as e:
        return json.loads(e.body)
    except urllib3.exceptions.MaxRetryError as e:
        raise e
    return result_dict


def thola_read_ups(host_ip, snmp_config, api_host):
    """Executes thola read ups on a given device."""
    body = thola_client.ReadUPSRequest(
        device_data=thola_client.DeviceData(
            ip_address=host_ip,
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[snmp_config.community],
                    versions=[snmp_config.version],
                    ports=[snmp_config.port],
                    discover_retries=snmp_config.discover_retries,
                    discover_timeout=snmp_config.discover_timeout,
                    discover_parallel_requests=snmp_config.discover_par_requests
                )
            )
        )
    )
    read_api = read.ReadApi()
    read_api.api_client.configuration.host = api_host
    try:
        result_dict = read_api.read_ups(body=body).to_dict()
    except rest.ApiException as e:
        return json.loads(e.body)
    except urllib3.exceptions.MaxRetryError as e:
        raise e
    return result_dict


def thola_identify(snmp_config, primary_ip):
    api_host = PLUGIN_SETTINGS["thola_api"]
    host_ip = normalize_ipv4(str(primary_ip))
    stderr = sys.stderr
    sys.stderr = None  # disable stderr during execution
    body = thola_client.IdentifyRequest(
        device_data=thola_client.DeviceData(
            ip_address=host_ip,
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[snmp_config.community],
                    versions=[snmp_config.version],
                    ports=[snmp_config.port],
                    discover_retries=snmp_config.discover_retries,
                    discover_timeout=snmp_config.discover_timeout,
                    discover_parallel_requests=snmp_config.discover_par_requests
                )
            )
        )
    )
    identify_api = identify.IdentifyApi()
    identify_api.api_client.configuration.host = api_host
    try:
        result_dict = identify_api.identify(body=body).to_dict()
    except rest.ApiException as e:
        sys.stderr = stderr  # enable stderr again
        return json.loads(e.body)
    except urllib3.exceptions.MaxRetryError:
        sys.stderr = stderr  # enable stderr again
        return {"error": "Connection to Thola API couldn't be established"}
    sys.stderr = stderr  # enable stderr again
    return result_dict
