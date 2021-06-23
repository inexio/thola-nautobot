import urllib3
import thola_client
import thola_client.api.read_api as read
import thola_client.rest as rest

from thola_nautobot.thola.snmp_config import SNMPConfig


def read_available_data(thola_device, api_host):
    """Reads data from the available components set on a given thola device."""
    snmp_config = SNMPConfig(thola_device)
    host_ip = str(thola_device.device.primary_ip4)
    results = {}
    if thola_device.cpu:
        results['cpu'] = thola_read_cpu_load(host_ip, snmp_config, api_host)
    if thola_device.disk:
        results['disk'] = thola_read_disk(host_ip, snmp_config, api_host)
    if thola_device.hardware_health:
        results['hardware_health'] = thola_read_hardware_health(host_ip, snmp_config, api_host)
    if thola_device.interfaces:
        results['interfaces'] = thola_read_interfaces(host_ip, snmp_config, api_host)
    if thola_device.memory:
        results['memory'] = thola_read_memory_usage(host_ip, snmp_config, api_host)
    if thola_device.sbc:
        results['sbc'] = thola_read_sbc(host_ip, snmp_config, api_host)
    if thola_device.server:
        results['server'] = thola_read_server(host_ip, snmp_config, api_host)
    if thola_device.ups:
        results['ups'] = thola_read_ups(host_ip, snmp_config, api_host)
    return results


def thola_read_available_components(thola_device, api_host):
    """Executes thola read available-components on a given device."""
    snmp_config = SNMPConfig(thola_device)
    host_ip = str(thola_device.device.primary_ip4)
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
        return {"error": e.body}
    except urllib3.exceptions.MaxRetryError as e:
        return {"error": e.reason}
    return result_dict


def thola_read_cpu_load(host_ip, snmp_config: SNMPConfig, api_host):
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
        return {"error": e.body}
    except urllib3.exceptions.MaxRetryError as e:
        return {"error": e.reason}
    return result_dict


def thola_read_disk(host_ip, snmp_config: SNMPConfig, api_host):
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
        return {"error": e.body}
    except urllib3.exceptions.MaxRetryError as e:
        return {"error": e.reason}
    return result_dict


def thola_read_hardware_health(host_ip, snmp_config: SNMPConfig, api_host):
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
        return {"error": e.body}
    except urllib3.exceptions.MaxRetryError as e:
        return {"error": e.reason}
    return result_dict


def thola_read_interfaces(host_ip, snmp_config: SNMPConfig, api_host):
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
        return {"error": e.body}
    except urllib3.exceptions.MaxRetryError as e:
        return {"error": e.reason}
    return result_dict


def thola_read_memory_usage(host_ip, snmp_config: SNMPConfig, api_host):
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
        return {"error": e.body}
    except urllib3.exceptions.MaxRetryError as e:
        return {"error": e.reason}
    return result_dict


def thola_read_sbc(host_ip, snmp_config: SNMPConfig, api_host):
    """Executes thola read sbc on a given device."""
    body = thola_client.ReadSBCRequest(
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
        result_dict = read_api.read_sbc(body=body).to_dict()
    except rest.ApiException as e:
        return {"error": e.body}
    except urllib3.exceptions.MaxRetryError as e:
        return {"error": e.reason}
    return result_dict


def thola_read_server(host_ip, snmp_config: SNMPConfig, api_host):
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
        return {"error": e.body}
    except urllib3.exceptions.MaxRetryError as e:
        return {"error": e.reason}
    return result_dict


def thola_read_ups(host_ip, snmp_config: SNMPConfig, api_host):
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
        return {"error": e.body}
    except urllib3.exceptions.MaxRetryError as e:
        return {"error": e.reason}
    return result_dict
