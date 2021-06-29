"""Template extensions for thola nautobot."""
from nautobot.extras.plugins import PluginTemplateExtension

from thola_nautobot.models import TholaDevice
from nautobot.dcim.models import Device


class DeviceStatusLink(PluginTemplateExtension):
    """Template extension to link device status on the right side of the page."""

    model = "dcim.device"

    def right_page(self):
        thola_device = TholaDevice.objects.filter(device=self.context["object"]).first()
        device = self.context["object"]

        if not thola_device:
            return self.render("thola_nautobot/device_extension_disabled.html", extra_context={
                "add_url": "/plugins/thola_nautobot/tholadevice/add?device=" + device.name
            })

        return self.render("thola_nautobot/device_extension.html", extra_context={
            "thola_device": thola_device
        })


template_extensions = [DeviceStatusLink]
