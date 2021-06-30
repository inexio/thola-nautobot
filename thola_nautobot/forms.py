"""Forms for thola nautobot."""
from django import forms
from django.conf import settings
from nautobot.dcim.models import Device

from thola_nautobot.models import TholaDevice
from thola_nautobot.thola.client import thola_read_available_components
from thola_nautobot.thola.snmp_config import SNMPConfig

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG["thola_nautobot"]


class TholaDeviceForm(forms.ModelForm):
    """Form for creating a new Thola Device instance."""

    device = forms.ModelChoiceField(
        queryset=Device.objects.all(),
        required=True,
        help_text="Device to monitor with Thola."
    )

    snmp_community = forms.CharField(
        required=False,
        label="SNMP community",
        help_text="Community string for SNMP to use. (def: " + str(PLUGIN_SETTINGS["snmp_community"]) + ")"
    )

    snmp_version = forms.CharField(
        required=False,
        label="SNMP version",
        help_text="SNMP version to use. (def: " + str(PLUGIN_SETTINGS["snmp_version"]) + ")"
    )

    snmp_port = forms.IntegerField(
        required=False,
        label="SNMP port",
        help_text="Port for SNMP to use. (def: " + str(PLUGIN_SETTINGS["snmp_port"]) + ")"
    )

    snmp_discover_par_requests = forms.IntegerField(
        required=False,
        label="SNMP discover par requests",
        help_text="The amount of parallel connection requests used while trying to get a valid SNMP connection. "
                  "(def: " + str(PLUGIN_SETTINGS["snmp_discover_par_requests"]) + ")"
    )

    snmp_discover_retries = forms.IntegerField(
        required=False,
        label="SNMP discover retries",
        help_text="The retries used while trying to get a valid SNMP connection. (def: " + str(PLUGIN_SETTINGS["snmp_discover_retries"]) + ")"
    )

    snmp_discover_timeout = forms.IntegerField(
        required=False,
        label="SNMP discover timeout",
        help_text="The timeout in seconds used while trying to get a valid SNMP connection. (def: " + str(PLUGIN_SETTINGS["snmp_discover_timeout"]) + ")"
    )

    http_password = forms.CharField(
        required=False,
        label="HTTP password",
        help_text="Password for HTTP/HTTPS authentication."
    )

    http_port = forms.IntegerField(
        required=False,
        label="HTTP port",
        help_text="Port for HTTP to use."
    )

    http_username = forms.CharField(
        required=False,
        label="HTTP username",
        help_text="Username for HTTP/HTTPS authentication."
    )

    https_port = forms.IntegerField(
        required=False,
        label="HTTPS port",
        help_text="Port for HTTPS to use."
    )

    class Meta:
        model = TholaDevice
        fields = [
            "device",
            "snmp_community",
            "snmp_version",
            "snmp_port",
            "snmp_discover_par_requests",
            "snmp_discover_retries",
            "snmp_discover_timeout",
            "http_password",
            "http_port",
            "http_username",
            "https_port"
        ]

    def save(self, commit=True, **kwargs):
        """Save the model and the associated components."""
        model = super().save(commit=False)

        snmp_config = SNMPConfig(model.snmp_community, model.snmp_version, model.snmp_port, model.snmp_discover_retries,
                                 model.snmp_discover_timeout, model.snmp_discover_par_requests)
        components = thola_read_available_components(snmp_config, model.device.primary_ip4)
        if components.get('error'):
            raise RuntimeError(components.get('error'))

        model.interfaces = "interfaces" in components.get('available_components')
        model.cpu = "cpu" in components.get('available_components')
        model.memory = "memory" in components.get('available_components')
        model.disk = "disk" in components.get('available_components')
        model.hardware_health = "hardware_health" in components.get('available_components')
        model.ups = "ups" in components.get('available_components')
        model.server = "server" in components.get('available_components')
        model.save()
        return model
