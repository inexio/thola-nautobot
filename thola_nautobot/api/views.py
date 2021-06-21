"""REST API views for thola nautobot."""
import urllib3
from rest_framework import viewsets
from rest_framework.request import Request
from django.http import JsonResponse

import thola_client
import thola_client.api.read_api as read
import thola_client.rest as rest

from thola_nautobot.models import TholaDevice


class ReadLiveData(viewsets.ViewSet):
    """API to read live data about a device."""

    queryset = TholaDevice.objects.all()  # TODO why do we need this?

    def get(self, request: Request):
        device_uuid = request.query_params["device"]
        response = {}
        return JsonResponse(response)


class ReadAvailableComponents(viewsets.ViewSet):
    """API to read all available components of a device."""

    def get(self, request: Request):
        device_uuid = request.query_params["device"]
        response = {}
        return JsonResponse(response)


def thola_read_available_components(host, api_host, community, port, version):
    """Executes thola read available-components on a given device."""
    body = thola_client.ReadAvailableComponentsRequest(
        device_data=thola_client.DeviceData(
            ip_address=host,
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[community],
                    versions=[version],
                    ports=[port],
                    discover_retries=0,
                    discover_timeout=2,
                    discover_parallel_requests=5
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


def thola_read_cpu_load(host, api_host, community, port, version):
    """Executes thola read cpu-load on a given device."""
    body = thola_client.ReadCPULoadRequest(
        device_data=thola_client.DeviceData(
            ip_address=host,
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[community],
                    versions=[version],
                    ports=[port],
                    discover_retries=0,
                    discover_timeout=2,
                    discover_parallel_requests=5
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


def thola_read_disk(host, api_host, community, port, version):
    """Executes thola read disk on a given device."""
    body = thola_client.ReadDiskRequest(
        device_data=thola_client.DeviceData(
            ip_address=host,
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[community],
                    versions=[version],
                    ports=[port],
                    discover_retries=0,
                    discover_timeout=2,
                    discover_parallel_requests=5
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


def thola_read_hardware_health(host, api_host, community, port, version):
    """Executes thola read hardware-health on a given device."""
    body = thola_client.ReadHardwareHealthRequest(
        device_data=thola_client.DeviceData(
            ip_address=host,
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[community],
                    versions=[version],
                    ports=[port],
                    discover_retries=0,
                    discover_timeout=2,
                    discover_parallel_requests=5
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


def thola_read_interfaces(host, api_host, community, port, version):
    """Executes thola read interfaces on a given device."""
    body = thola_client.ReadInterfacesRequest(
        device_data=thola_client.DeviceData(
            ip_address=host,
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[community],
                    versions=[version],
                    ports=[port],
                    discover_retries=0,
                    discover_timeout=2,
                    discover_parallel_requests=5
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


def thola_read_memory_usage(host, api_host, community, port, version):
    """Executes thola read memory-usage on a given device."""
    body = thola_client.ReadMemoryUsageRequest(
        device_data=thola_client.DeviceData(
            ip_address=host,
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[community],
                    versions=[version],
                    ports=[port],
                    discover_retries=0,
                    discover_timeout=2,
                    discover_parallel_requests=5
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


def thola_read_sbc(host, api_host, community, port, version):
    """Executes thola read sbc on a given device."""
    body = thola_client.ReadSBCRequest(
        device_data=thola_client.DeviceData(
            ip_address=host,
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[community],
                    versions=[version],
                    ports=[port],
                    discover_retries=0,
                    discover_timeout=2,
                    discover_parallel_requests=5
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


def thola_read_server(host, api_host, community, port, version):
    """Executes thola read server on a given device."""
    body = thola_client.ReadServerRequest(
        device_data=thola_client.DeviceData(
            ip_address=host,
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[community],
                    versions=[version],
                    ports=[port],
                    discover_retries=0,
                    discover_timeout=2,
                    discover_parallel_requests=5
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


def thola_read_ups(host, api_host, community, port, version):
    """Executes thola read ups on a given device."""
    body = thola_client.ReadUPSRequest(
        device_data=thola_client.DeviceData(
            ip_address=host,
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[community],
                    versions=[version],
                    ports=[port],
                    discover_retries=0,
                    discover_timeout=2,
                    discover_parallel_requests=5
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
