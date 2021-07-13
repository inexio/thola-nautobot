"""REST API serializers for thola nautobot."""
from nautobot.dcim.api.serializers import DeviceSerializer, SiteSerializer, DeviceRoleSerializer
from rest_framework import serializers
from thola_nautobot.models import TholaConfig, TholaOnboarding


class TholaConfigSerializer(serializers.ModelSerializer):
    """Serializer for config API."""

    device = DeviceSerializer

    class Meta:
        """Meta class for TholaConfigSerializer."""

        model = TholaConfig
        fields = ["id", "device", "snmp_community", "snmp_version", "snmp_port", "snmp_discover_par_requests",
                  "snmp_discover_retries", "snmp_discover_timeout", "http_password", "http_port", "http_username",
                  "https_port"]


class TholaOnboardingSerializer(serializers.ModelSerializer):
    """Serializer for onboarding API."""

    device = DeviceSerializer
    site = SiteSerializer
    role = DeviceRoleSerializer

    class Meta:
        """Meta class for TholaOnboardingSerializer."""

        model = TholaOnboarding
        fields = ["id", "device", "ip", "site", "role", "snmp_community", "snmp_version", "snmp_port",
                  "snmp_discover_par_requests", "snmp_discover_retries", "snmp_discover_timeout", "status"]
