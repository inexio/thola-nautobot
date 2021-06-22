"""REST API serializers for thola nautobot."""
from nautobot.dcim.api.serializers import DeviceSerializer
from rest_framework import serializers
from thola_nautobot.models import TholaDevice


class TholaDeviceSerializer(serializers.ModelSerializer):
    """Serializer for API."""

    device = DeviceSerializer

    class Meta:
        """Meta class for TholaDeviceSerializer."""

        model = TholaDevice
        fields = ["id", "device", "snmp_community", "snmp_version", "snmp_port", "snmp_discover_par_requests",
                  "snmp_discover_retries", "snmp_discover_timeout", "http_password", "http_port", "http_username",
                  "https_port"]
