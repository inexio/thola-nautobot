"""REST API views for thola nautobot."""
from django.shortcuts import get_object_or_404
from nautobot.core.api.exceptions import ServiceUnavailable
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from thola_nautobot.thola.client import read_available_data
from thola_nautobot.api.serializers import TholaDeviceSerializer
from thola_nautobot.models import TholaDevice


class TholaDeviceViews(ModelViewSet):
    """API view for thola device operations."""

    queryset = TholaDevice.objects.all()
    serializer_class = TholaDeviceSerializer

    @action(detail=True, url_path="livedata")
    def livedata(self, _, pk):
        """Read all available live data of a given device."""
        thola_device = get_object_or_404(self.queryset, pk=pk)
        if thola_device.device.primary_ip4 is None:
            raise ServiceUnavailable("No IP is set for the device " + thola_device.device.name)

        results = read_available_data(thola_device)

        if results.get('error'):
            raise ServiceUnavailable(results.get('error'))

        return Response(results)
