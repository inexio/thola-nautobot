"""REST API views for thola nautobot."""
from django.shortcuts import get_object_or_404
from nautobot.core.api.exceptions import ServiceUnavailable
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import urllib3

import thola_client
import thola_client.api.read_api as read
import thola_client.rest as rest
from thola_nautobot.api.serializers import TholaDeviceSerializer
from thola_nautobot.models import TholaDevice
from thola_nautobot import config


class TholaDeviceViews(ModelViewSet):
    """API view for thola device operations."""

    queryset = TholaDevice.objects.all()
    serializer_class = TholaDeviceSerializer

    @action(detail=True, url_path="livedata")
    def livedata(self, _, pk):
        """Read all available live data of a given device."""
        thola_device = get_object_or_404(self.queryset, pk=pk)
        if thola_device.device.primary_ip4 is None:
            raise ServiceUnavailable("No IP is set for the device " + thola_device.device.name)

        snmp_port, discover_retries, discover_timeout, discover_par_requests, api_host = get_device_data(thola_device)

        results = read_all_data(thola_device, snmp_port, discover_retries, discover_timeout, discover_par_requests,
                                api_host)

        return Response(results)

    @action(detail=True, url_path="components")
    def components(self, _, pk):
        """Read all available live data of a given device."""
        thola_device: TholaDevice = get_object_or_404(self.queryset, pk=pk)
        if thola_device.device.primary_ip4 is None:
            raise ServiceUnavailable("No IP is set for the device " + thola_device.device.name)

        snmp_port, discover_retries, discover_timeout, discover_par_requests, api_host = get_device_data(thola_device)

        results = thola_read_available_components(thola_device, snmp_port, discover_retries, discover_timeout,
                                                  discover_par_requests, api_host)

        return Response(results)


def read_all_data(thola_device, snmp_port, discover_retries, discover_timeout, discover_par_requests, api_host):
    results = {}
    if thola_device.cpu:
        results['cpu'] = thola_read_cpu_load(thola_device, snmp_port, discover_retries, discover_timeout,
                                             discover_par_requests, api_host)
    if thola_device.disk:
        results['disk'] = thola_read_disk(thola_device, snmp_port, discover_retries, discover_timeout,
                                          discover_par_requests, api_host)
    if thola_device.hardware_health:
        results['hardware_health'] = thola_read_hardware_health(thola_device, snmp_port, discover_retries,
                                                                discover_timeout, discover_par_requests, api_host)
    if thola_device.interfaces:
        results['interfaces'] = thola_read_interfaces(thola_device, snmp_port, discover_retries, discover_timeout,
                                                      discover_par_requests, api_host)
    if thola_device.memory:
        results['memory'] = thola_read_memory_usage(thola_device, snmp_port, discover_retries, discover_timeout,
                                                    discover_par_requests, api_host)
    if thola_device.sbc:
        results['sbc'] = thola_read_sbc(thola_device, snmp_port, discover_retries, discover_timeout,
                                        discover_par_requests, api_host)
    if thola_device.server:
        results['server'] = thola_read_server(thola_device, snmp_port, discover_retries, discover_timeout,
                                              discover_par_requests, api_host)
    if thola_device.ups:
        results['ups'] = thola_read_ups(thola_device, snmp_port, discover_retries, discover_timeout,
                                        discover_par_requests, api_host)
    return results


def get_device_data(thola_device: TholaDevice):
    snmp_port, discover_retries, discover_timeout, discover_par_requests = 161, 0, 2, 5
    if thola_device.snmp_port is not None:
        snmp_port = thola_device.snmp_version
    if thola_device.snmp_discover_retries is not None:
        discover_retries = thola_device.snmp_discover_retries
    if thola_device.snmp_discover_timeout is not None:
        discover_timeout = thola_device.snmp_discover_timeout
    if thola_device.snmp_discover_par_requests is not None:
        discover_par_requests = thola_device.snmp_discover_par_requests
    api_host = config.default_settings['thola_api']
    return snmp_port, discover_retries, discover_timeout, discover_par_requests, api_host


def thola_read_available_components(thola_device, snmp_port, discover_retries, discover_timeout,
                                    discover_par_requests, api_host):
    """Executes thola read available-components on a given device."""
    body = thola_client.ReadAvailableComponentsRequest(
        device_data=thola_client.DeviceData(
            ip_address=str(thola_device.device.primary_ip4),
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[thola_device.snmp_community],
                    versions=[thola_device.snmp_version],
                    ports=[snmp_port],
                    discover_retries=discover_retries,
                    discover_timeout=discover_timeout,
                    discover_parallel_requests=discover_par_requests
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


def thola_read_cpu_load(thola_device, snmp_port, discover_retries, discover_timeout,
                        discover_par_requests, api_host):
    """Executes thola read cpu-load on a given device."""
    body = thola_client.ReadCPULoadRequest(
        device_data=thola_client.DeviceData(
            ip_address=str(thola_device.device.primary_ip4),
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[thola_device.snmp_community],
                    versions=[thola_device.snmp_version],
                    ports=[snmp_port],
                    discover_retries=discover_retries,
                    discover_timeout=discover_timeout,
                    discover_parallel_requests=discover_par_requests
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


def thola_read_disk(thola_device, snmp_port, discover_retries, discover_timeout,
                    discover_par_requests, api_host):
    """Executes thola read disk on a given device."""
    body = thola_client.ReadDiskRequest(
        device_data=thola_client.DeviceData(
            ip_address=str(thola_device.device.primary_ip4),
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[thola_device.snmp_community],
                    versions=[thola_device.snmp_version],
                    ports=[snmp_port],
                    discover_retries=discover_retries,
                    discover_timeout=discover_timeout,
                    discover_parallel_requests=discover_par_requests
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


def thola_read_hardware_health(thola_device, snmp_port, discover_retries, discover_timeout,
                               discover_par_requests, api_host):
    """Executes thola read hardware-health on a given device."""
    body = thola_client.ReadHardwareHealthRequest(
        device_data=thola_client.DeviceData(
            ip_address=str(thola_device.device.primary_ip4),
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[thola_device.snmp_community],
                    versions=[thola_device.snmp_version],
                    ports=[snmp_port],
                    discover_retries=discover_retries,
                    discover_timeout=discover_timeout,
                    discover_parallel_requests=discover_par_requests
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


def thola_read_interfaces(thola_device, snmp_port, discover_retries, discover_timeout,
                          discover_par_requests, api_host):
    """Executes thola read interfaces on a given device."""
    body = thola_client.ReadInterfacesRequest(
        device_data=thola_client.DeviceData(
            ip_address=str(thola_device.device.primary_ip4),
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[thola_device.snmp_community],
                    versions=[thola_device.snmp_version],
                    ports=[snmp_port],
                    discover_retries=discover_retries,
                    discover_timeout=discover_timeout,
                    discover_parallel_requests=discover_par_requests
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


def thola_read_memory_usage(thola_device, snmp_port, discover_retries, discover_timeout,
                            discover_par_requests, api_host):
    """Executes thola read memory-usage on a given device."""
    body = thola_client.ReadMemoryUsageRequest(
        device_data=thola_client.DeviceData(
            ip_address=str(thola_device.device.primary_ip4),
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[thola_device.snmp_community],
                    versions=[thola_device.snmp_version],
                    ports=[snmp_port],
                    discover_retries=discover_retries,
                    discover_timeout=discover_timeout,
                    discover_parallel_requests=discover_par_requests
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


def thola_read_sbc(thola_device, snmp_port, discover_retries, discover_timeout,
                   discover_par_requests, api_host):
    """Executes thola read sbc on a given device."""
    body = thola_client.ReadSBCRequest(
        device_data=thola_client.DeviceData(
            ip_address=str(thola_device.device.primary_ip4),
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[thola_device.snmp_community],
                    versions=[thola_device.snmp_version],
                    ports=[snmp_port],
                    discover_retries=discover_retries,
                    discover_timeout=discover_timeout,
                    discover_parallel_requests=discover_par_requests
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


def thola_read_server(thola_device, snmp_port, discover_retries, discover_timeout,
                      discover_par_requests, api_host):
    """Executes thola read server on a given device."""
    body = thola_client.ReadServerRequest(
        device_data=thola_client.DeviceData(
            ip_address=str(thola_device.device.primary_ip4),
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[thola_device.snmp_community],
                    versions=[thola_device.snmp_version],
                    ports=[snmp_port],
                    discover_retries=discover_retries,
                    discover_timeout=discover_timeout,
                    discover_parallel_requests=discover_par_requests
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


def thola_read_ups(thola_device, snmp_port, discover_retries, discover_timeout,
                   discover_par_requests, api_host):
    """Executes thola read ups on a given device."""
    body = thola_client.ReadUPSRequest(
        device_data=thola_client.DeviceData(
            ip_address=str(thola_device.device.primary_ip4),
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[thola_device.snmp_community],
                    versions=[thola_device.snmp_version],
                    ports=[snmp_port],
                    discover_retries=discover_retries,
                    discover_timeout=discover_timeout,
                    discover_parallel_requests=discover_par_requests
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
