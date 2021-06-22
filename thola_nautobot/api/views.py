"""REST API views for thola nautobot."""
import urllib3
from django.shortcuts import get_object_or_404
from nautobot.core.api.exceptions import ServiceUnavailable
from rest_framework.decorators import action

import thola_client
import thola_client.api.read_api as read
import thola_client.rest as rest
from rest_framework.viewsets import ModelViewSet

from thola_nautobot.api.serializers import TholaDeviceSerializer
from thola_nautobot.models import TholaDevice


class TholaDeviceViews(ModelViewSet):
    """API view for thola device operations."""

    queryset = TholaDevice.objects.all()
    serializer_class = TholaDeviceSerializer

    @action(detail=True, url_path="livedata")
    def livedata(self, request, pk):
        """Read all available live data of a given device."""

        thola_device = get_object_or_404(self.queryset, pk=pk)
        if not thola_device:
            raise ServiceUnavailable("This device does not exist.")
        raise ServiceUnavailable("This device " + thola_device.device.name + " does exist.")


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
