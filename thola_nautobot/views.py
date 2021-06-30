"""Views for thola nautobot."""
from django.shortcuts import render
from nautobot.core.views import generic
from nautobot.utilities.forms import restrict_form_fields
from nautobot.utilities.utils import normalize_querydict

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

    def get(self, request, *args, **kwargs):
        obj = self.alter_obj(self.get_object(kwargs), request, args, kwargs)

        initial_data = normalize_querydict(request.GET)
        form = self.model_form(instance=obj, initial=initial_data)
        restrict_form_fields(form, request.user)

        return render(request, "thola_nautobot/tholadevice_edit.html",
                      {
                          "obj": obj,
                          "obj_type": self.queryset.model._meta.verbose_name,
                          "form": form,
                          "return_url": self.get_return_url(request, obj),
                          "editing": obj.present_in_database,
                      },
                      )


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
            "livedata_url": "/api/plugins/thola_nautobot/tholadevice/{}/livedata/".format(instance.pk)
        }
