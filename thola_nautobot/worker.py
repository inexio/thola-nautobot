"""Worker for thola nautobot."""
from django.db import IntegrityError
from django_rq import job
from django.conf import settings
from nautobot.ipam.models import IPAddress

from thola_nautobot.choices import TholaOnboardingStatusChoice
from thola_nautobot.models import TholaConfig
from thola_nautobot.thola.client import thola_identify, thola_read_available_components
from thola_nautobot.thola.snmp_config import SNMPConfig

from nautobot.dcim.models import DeviceType, Manufacturer, Device, Interface
from django.core.exceptions import ObjectDoesNotExist
from nautobot.extras.models import Status

from thola_nautobot.thola.utils import normalize_ipv4, get_prefixlength

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

    # retrieve device_type
    if properties["properties"]["model"] is None:
        onboarding.status = TholaOnboardingStatusChoice.STATUS_FAILED
        onboarding.error_message = "Thola couldn't find a model for the device"
        onboarding.save()
        return
    model_name = properties["properties"]["model"]
    try:
        device_type = DeviceType.objects.get(model=model_name)
    except ObjectDoesNotExist:
        if not bool(PLUGIN_SETTINGS["onboarding_create_models"]):
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
        class_name = class_name.replace("/", "-")

        # retrieve manufacturer
        if properties["properties"]["vendor"] is None:
            onboarding.status = TholaOnboardingStatusChoice.STATUS_FAILED
            onboarding.error_message = "Thola couldn't find the vendor of the device"
            onboarding.save()
            return
        vendor_name = properties["properties"]["vendor"]
        try:
            vendor = Manufacturer.objects.get(name=vendor_name)
        except ObjectDoesNotExist:
            vendor = Manufacturer.objects.create(name=vendor_name, slug=vendor_name.lower().replace(" ", "-"),
                                                 description="Automatically created with Thola")
        device_type = DeviceType.objects.create(manufacturer=vendor, model=model_name, slug=class_name, u_height=1,
                                                comments="Automatically created with Thola")

    device_role = onboarding.role
    status = Status.objects.get(name="Active")
    device = Device.objects.create(device_role=device_role, device_type=device_type, site=site, status=status)

    # retrieve serial number
    serial_number = None
    if properties["properties"]["serial_number"] is not None:
        serial_number = properties["properties"]["serial_number"]
        device.serial = serial_number
        device.save()

    # set device name if enabled
    if bool(PLUGIN_SETTINGS["onboarding_device_name"]):
        name = create_name(device_type.manufacturer.name, serial_number, primary_ip)
        device.name = name
        device.save()

    # create ipaddress
    try:
        ip_address = IPAddress.objects.get(host=normalize_ipv4(primary_ip))
    except ObjectDoesNotExist:
        ip_address = IPAddress.objects.create(host=normalize_ipv4(primary_ip),
                                              prefix_length=get_prefixlength(primary_ip))

    # create interface
    interface = Interface.objects.create(name="main", device_id=device.pk)
    interface.ip_addresses.set([ip_address])
    device.primary_ip4 = ip_address

    ip_address.save()
    try:
        device.save()
    except IntegrityError:
        onboarding.status = TholaOnboardingStatusChoice.STATUS_WARNING
        onboarding.error_message = "Couldn't assign the IP address. Already in use."
        onboarding.save()
        return

    # create thola config
    create_thola_config(snmp_config, device)

    onboarding.status = TholaOnboardingStatusChoice.STATUS_SUCCESS
    onboarding.error_message = None
    onboarding.save()


def create_thola_config(snmp_config, device):
    """Create a TholaConfig with the given snmp_config. Set the components accordingly."""
    components = thola_read_available_components(snmp_config, device.primary_ip4)
    if components.get('error'):
        raise RuntimeError(components.get('error'))

    interfaces = "interfaces" in components.get('available_components')
    cpu = "cpu" in components.get('available_components')
    memory = "memory" in components.get('available_components')
    disk = "disk" in components.get('available_components')
    hardware_health = "hardware_health" in components.get('available_components')
    ups = "ups" in components.get('available_components')
    server = "server" in components.get('available_components')

    TholaConfig.objects.create(device=device, snmp_community=snmp_config.community,
                               snmp_version=snmp_config.version, snmp_port=snmp_config.port,
                               snmp_discover_par_requests=snmp_config.discover_par_requests,
                               snmp_discover_retries=snmp_config.discover_retries,
                               snmp_discover_timeout=snmp_config.discover_timeout,
                               interfaces=interfaces, cpu=cpu, memory=memory, disk=disk,
                               hardware_health=hardware_health, ups=ups, server=server)


def create_name(vendor, serial_number, primary_ip):
    """Create a name for a device based on vendor, model, serial_number and ip."""
    if serial_number is not None:
        return vendor[:2].upper() + serial_number
    return vendor[:2].upper() + normalize_ipv4(primary_ip)
