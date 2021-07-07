"""Worker for thola nautobot."""
from django_rq import job
from django.conf import settings
from thola_nautobot.choices import TholaOnboardingStatusChoice
from thola_nautobot.thola.client import thola_identify
from thola_nautobot.thola.snmp_config import SNMPConfig

from nautobot.dcim.models import DeviceType, Manufacturer, Device
from django.core.exceptions import ObjectDoesNotExist
from nautobot.extras.models import Status

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG["thola_nautobot"]


@job('default')
def onboard_device(onboarding):
    """Onboard device based on site_id and primary_ip."""
    onboarding.status = TholaOnboardingStatusChoice.STATUS_RUNNING
    onboarding.save()
    primary_ip = onboarding.ip
    site = onboarding.site
    snmp_config = SNMPConfig(community=onboarding.snmp_community,
                             version=onboarding.snmp_version,
                             port=onboarding.snmp_port,
                             discover_retries=onboarding.snmp_discover_retries,
                             discover_timeout=onboarding.snmp_discover_timeout,
                             discover_par_requests=onboarding.snmp_discover_par_requests)
    properties = thola_identify(snmp_config, primary_ip)
    if "error" in properties.keys():
        onboarding.status = TholaOnboardingStatusChoice.STATUS_FAILED
        onboarding.error_message = properties["error"]
        onboarding.save()
        return
    if properties["properties"]["model"] is None:
        onboarding.status = TholaOnboardingStatusChoice.STATUS_FAILED
        onboarding.error_message = "Thola couldn't find a model for the device"
        onboarding.save()
        return
    model_name = properties["properties"]["model"]
    try:
        device_type = DeviceType.objects.get(model=model_name)
    except ObjectDoesNotExist:
        if not PLUGIN_SETTINGS["onboarding_create_models"]:
            onboarding.status = TholaOnboardingStatusChoice.STATUS_FAILED
            onboarding.error_message = "The plugin's settings don't allow to create new device types / manufacturers"
            onboarding.save()
            return
        if properties["_class"] is None:
            onboarding.status = TholaOnboardingStatusChoice.STATUS_FAILED
            onboarding.error_message = "Thola didn't return a device class"
            onboarding.save()
            return
        class_name = properties["_class"]
        class_name = class_name.replace("/", "_")
        if properties["properties"]["vendor"] is None:
            onboarding.status = TholaOnboardingStatusChoice.STATUS_FAILED
            onboarding.error_message = "Thola couldn't find the vendor of the device"
            onboarding.save()
            return
        vendor_name = properties["properties"]["vendor"]
        try:
            vendor = Manufacturer.objects.get(name=vendor_name)
        except ObjectDoesNotExist:
            vendor = Manufacturer.objects.create(name=vendor_name, slug=vendor_name.lower(),
                                                 description="Automatically created with Thola")
        device_type = DeviceType.objects.create(manufacturer=vendor, model=model_name, slug=class_name, u_height=1,
                                                comments="Automatically created with Thola")
    device_role = onboarding.role
    status = Status.objects.get(name="Active")
    Device.objects.create(device_role=device_role, device_type=device_type, site=site, status=status)
    onboarding.status = TholaOnboardingStatusChoice.STATUS_SUCCESS
    onboarding.error_message = None
    onboarding.save()
