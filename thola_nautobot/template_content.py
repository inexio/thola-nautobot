"""Template extensions for thola nautobot."""
from nautobot.dcim.models import Device, DeviceType
from nautobot.extras.plugins import PluginTemplateExtension

from thola_nautobot.models import TholaConfig


class DeviceStatusLink(PluginTemplateExtension):
    """Template extension to link device status on the right side of the page."""

    model = "dcim.device"

    def right_page(self):
        thola_config = TholaConfig.objects.filter(device=self.context["object"]).first()
        device: Device = self.context["object"]
        device_type: DeviceType = device.device_type
        if not device.name:
            device_name = device_type.manufacturer.name + " " + device_type.model + " (" + str(device.pk) + ")"
        else:
            device_name = device.name
        if not thola_config:
            return self.render("thola_nautobot/device_extension_disabled.html", extra_context={
                "add_url": "/plugins/thola_nautobot/config/add?device=" + device_name
            })

        return self.render("thola_nautobot/device_extension.html", extra_context={
            "thola_config": thola_config
        })


template_extensions = [DeviceStatusLink]
