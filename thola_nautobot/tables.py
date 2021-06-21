"""Tables for thola nautobot."""
import django_tables2 as tables

from nautobot.utilities.tables import BaseTable, ToggleColumn

from .models import TholaDevice


class TholaDeviceTable(BaseTable):
    """Table for thola devices."""

    pk = ToggleColumn()
    id = tables.LinkColumn()
    device = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        """Meta for class TholaDeviceTable."""

        model = TholaDevice
        fields = (
            "pk",
            "id",
            "device",
            "snmp_community",
            "snmp_version",
            "snmp_port",
            "http_password",
            "http_port",
            "http_username",
            "https_port",
        )
