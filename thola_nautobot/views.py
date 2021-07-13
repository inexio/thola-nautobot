"""Views for thola nautobot."""
from django.shortcuts import render
from nautobot.core.views import generic
from nautobot.utilities.forms import restrict_form_fields
from nautobot.utilities.utils import normalize_querydict

from . import models, tables, forms
from .models import TholaConfig

"""
Thola Config
"""


class TholaConfigListView(generic.ObjectListView):
    """View for listing all thola configs."""

    queryset = models.TholaConfig.objects.all()
    table = tables.TholaConfigTable
    template_name = "thola_nautobot/tholaconfig_list.html"


class TholaConfigView(generic.ObjectView):
    """Detailed view for a specific thola config."""

    queryset = models.TholaConfig.objects.all()
    template_name = "thola_nautobot/tholaconfig.html"


class TholaConfigEditView(generic.ObjectEditView):
    """View for editing a thola config."""

    model = models.TholaConfig
    queryset = models.TholaConfig.objects.all()
    model_form = forms.TholaConfigForm

    def get(self, request, *args, **kwargs):
        obj = self.alter_obj(self.get_object(kwargs), request, args, kwargs)

        initial_data = normalize_querydict(request.GET)
        form = self.model_form(instance=obj, initial=initial_data)
        restrict_form_fields(form, request.user)

        return render(request, "thola_nautobot/tholaconfig_edit.html",
                      {
                          "obj": obj,
                          "obj_type": self.queryset.model._meta.verbose_name,
                          "form": form,
                          "return_url": self.get_return_url(request, obj),
                          "editing": obj.present_in_database,
                      },
                      )


class TholaConfigDeleteView(generic.ObjectDeleteView):
    """View for deleting a thola config."""

    queryset = models.TholaConfig.objects.all()


class TholaConfigBulkDeleteView(generic.BulkDeleteView):
    """View for deleting many thola configs at once."""

    queryset = models.TholaConfig.objects.filter()
    table = tables.TholaConfigTable
    default_return_url = "plugins:thola_nautobot:tholaconfig_list"


class TholaConfigStatusView(generic.ObjectView):
    """Detailed view for live status of a thola config."""

    queryset = TholaConfig.objects.all()
    template_name = "thola_nautobot/tholastatus.html"

    def get_extra_context(self, request, instance):
        """Add extra data to status view of a thola config."""

        return {
            "livedata_url": "/api/plugins/thola_nautobot/config/{}/livedata/".format(instance.pk)
        }


"""
Thola Onboarding
"""


class TholaOnboardingListView(generic.ObjectListView):
    """View for listing all thola onboarding tasks."""

    queryset = models.TholaOnboarding.objects.all()
    table = tables.TholaOnboardingTable
    template_name = "thola_nautobot/tholaonboarding_list.html"


class TholaOnboardingView(generic.ObjectView):
    """Detailed view for a specific thola onboarding task."""

    queryset = models.TholaOnboarding.objects.all()
    template_name = "thola_nautobot/tholaonboarding.html"

    def get_extra_context(self, request, instance):
        """Add extra data to detail view of a thola onboarding."""

        return {
            "onboard_url": "/api/plugins/thola_nautobot/onboarding/{}/onboard/".format(instance.pk)
        }


class TholaOnboardingEditView(generic.ObjectEditView):
    """View for editing a thola onboarding task."""

    model = models.TholaOnboarding
    queryset = models.TholaOnboarding.objects.all()
    model_form = forms.TholaOnboardingForm


class TholaOnboardingDeleteView(generic.ObjectDeleteView):
    """View for deleting a thola onboarding task."""

    queryset = models.TholaOnboarding.objects.all()


class TholaOnboardingBulkDeleteView(generic.BulkDeleteView):
    """View for deleting many thola onboarding tasks at once."""

    queryset = models.TholaOnboarding.objects.filter()
    table = tables.TholaOnboardingTable
    default_return_url = "plugins:thola_nautobot:tholaonboarding_list"
