"""Forms for thola_nautobot."""
from django import forms
from nautobot.dcim.models import Device

from thola_nautobot.models import TholaDevice


class TholaDeviceForm(forms.ModelForm):
    """Form for creating a new Thola Device instance."""

    device = forms.ModelChoiceField(
        queryset=Device.objects.all(),
        required=True,
        help_text="Device to monitor with Thola."
    )

    snmp_community = forms.CharField(
        required=True,
        label="SNMP community",
        help_text="Community string for SNMP to use. (def: public)"
    )

    snmp_version = forms.CharField(
        required=True,
        label="SNMP version",
        help_text="SNMP version to use. (def: 2c)"
    )

    snmp_port = forms.IntegerField(
        required=False,
        label="SNMP port",
        help_text="Port for SNMP to use. (def: 161)"
    )

    snmp_discover_par_requests = forms.IntegerField(
        required=False,
        label="SNMP discover par requests",
        help_text="The amount of parallel connection requests used while trying to get a valid SNMP connection. "
                  "(def: 5)"
    )

    snmp_discover_retries = forms.IntegerField(
        required=False,
        label="SNMP discover retries",
        help_text="The retries used while trying to get a valid SNMP connection. (def: 0)"
    )

    snmp_discover_timeout = forms.IntegerField(
        required=False,
        label="SNMP discover timeout",
        help_text="The timeout in seconds used while trying to get a valid SNMP connection. (def: 2)")

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
        super().save(commit=commit)
        device: Device = Device.objects.get(self.device)
        print(device.name)
