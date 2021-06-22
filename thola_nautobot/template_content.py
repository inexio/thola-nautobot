"""Template extensions for thola nautobot."""
from nautobot.extras.plugins import PluginTemplateExtension

from thola_nautobot.models import TholaDevice


class DeviceStatusLink(PluginTemplateExtension):
    """Template extension to link device status on the right side of the page."""

    model = "dcim.device"

    def right_page(self):
        thola_device = TholaDevice.objects.filter(device=self.context["object"]).first()

        if not thola_device:
            return self.render("thola_nautobot/device_extension_disabled.html")

        return self.render("thola_nautobot/device_extension.html", extra_context={
            "thola_device": thola_device
        })


template_extensions = [DeviceStatusLink]
