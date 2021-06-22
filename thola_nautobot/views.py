"""Views for thola nautobot."""
from nautobot.core.views import generic

from . import models, tables, forms
from .models import TholaDevice


class TholaDeviceListView(generic.ObjectListView):
    """View for listing all thola devices."""

    queryset = models.TholaDevice.objects.all()
    table = tables.TholaDeviceTable
    action_buttons = {"add"}


class TholaDeviceView(generic.ObjectView):
    """Detailed view for a specific thola device."""

    queryset = models.TholaDevice.objects.all()
    template_name = "thola_nautobot/tholadevice.html"


class TholaDeviceEditView(generic.ObjectEditView):
    """View for editing a thola device."""

    model = models.TholaDevice
    queryset = models.TholaDevice.objects.all()
    model_form = forms.TholaDeviceForm


class TholaDeviceDeleteView(generic.ObjectDeleteView):
    """View for deleting a thola device."""

    queryset = models.TholaDevice.objects.all()


class TholaDeviceStatusView(generic.ObjectView):
    """Detailed view for live status of a thola device."""

    queryset = TholaDevice.objects.all()
    template_name = "thola_nautobot/tholastatus.html"

    def get_extra_context(self, request, instance):
        """Add extra data to status view of a thola device."""

        return {
            "livedata_url": "/api/plugins/thola_nautobot/tholadevice/{}/livedata".format(instance.pk)
        }
