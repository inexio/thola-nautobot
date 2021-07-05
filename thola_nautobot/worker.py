"""Worker for thola nautobot."""
from django_rq import job


@job('default')
def onboard_device(site_id, primary_ip):
    """Onboard device based on site_id and primary_ip."""
    # TODO
