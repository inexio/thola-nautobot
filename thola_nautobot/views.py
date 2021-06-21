"""Views for thola_nautobot."""
from nautobot.core.views import generic
from nautobot.dcim import models

from . import models, tables, forms


class TholaDeviceListView(generic.ObjectListView):
    """View for listing all thola devices."""

    queryset = models.TholaDevice.objects.all()
    table = tables.TholaDeviceTable
    action_buttons = {"add"}


class TholaDeviceView(generic.ObjectView):
    """Detailed view for a specific thola device."""

    queryset = models.TholaDevice.objects.all()

    def get_extra_context(self, request, instance):
        """Extend content of detailed view for a specific thola device."""

        device = models.TholaDevice.objects.filter()  # TODO: get device reference for thola device

        return {
            "device": device
        }


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
    # TODO
