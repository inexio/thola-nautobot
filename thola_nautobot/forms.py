"""Forms for thola nautobot."""
import django_rq
from django import forms
from django.conf import settings
from nautobot.dcim.models import Device, Site, DeviceRole

from thola_nautobot.choices import TholaOnboardingStatusChoice
from thola_nautobot.models import TholaConfig, TholaOnboarding
from thola_nautobot.thola.client import thola_read_available_components
from thola_nautobot.thola.snmp_config import SNMPConfig

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG["thola_nautobot"]


class TholaConfigForm(forms.ModelForm):
    """Form for creating a new Thola Config instance."""

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
        help_text="The retries used while trying to get a valid SNMP connection. (def: " + str(
            PLUGIN_SETTINGS["snmp_discover_retries"]) + ")"
    )

    snmp_discover_timeout = forms.IntegerField(
        required=False,
        label="SNMP discover timeout",
        help_text="The timeout in seconds used while trying to get a valid SNMP connection. (def: " + str(
            PLUGIN_SETTINGS["snmp_discover_timeout"]) + ")"
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
        model = TholaConfig
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


class TholaOnboardingForm(forms.ModelForm):
    """Form for creating a new Thola Onboarding task."""

    ip = forms.CharField(
        required=True,
        label="IP address",
        help_text="IP address of the device."
    )

    site = forms.ModelChoiceField(
        queryset=Site.objects.all(),
        required=True,
        help_text="Site of the device."
    )

    role = forms.ModelChoiceField(
        queryset=DeviceRole.objects.all(),
        required=True,
        help_text="Role of the device."
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
        help_text="The retries used while trying to get a valid SNMP connection. (def: " + str(
            PLUGIN_SETTINGS["snmp_discover_retries"]) + ")"
    )

    snmp_discover_timeout = forms.IntegerField(
        required=False,
        label="SNMP discover timeout",
        help_text="The timeout in seconds used while trying to get a valid SNMP connection. (def: " + str(
            PLUGIN_SETTINGS["snmp_discover_timeout"]) + ")"
    )

    class Meta:
        model = TholaOnboarding
        fields = [
            "ip",
            "site",
            "role",
            "snmp_community",
            "snmp_version",
            "snmp_port",
            "snmp_discover_par_requests",
            "snmp_discover_retries",
            "snmp_discover_timeout"
        ]

    def save(self, commit=True, **kwargs):
        """Save the model and the associated components."""
        model = super().save(commit=False)

        model.status = TholaOnboardingStatusChoice.STATUS_PENDING
        model.save()

        queue = django_rq.get_queue('default')
        queue.enqueue("thola_nautobot.worker.onboard_device", onboarding=model)
        return model
