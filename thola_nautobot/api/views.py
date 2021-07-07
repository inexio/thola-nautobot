"""REST API views for thola nautobot."""
import django_rq
from django.shortcuts import get_object_or_404
from nautobot.core.api.exceptions import ServiceUnavailable
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from thola_nautobot.thola.client import read_available_data
from thola_nautobot.api.serializers import TholaConfigSerializer, TholaOnboardingSerializer
from thola_nautobot.models import TholaConfig, TholaOnboarding


class TholaConfigViews(ModelViewSet):
    """API view for thola config operations."""

    queryset = TholaConfig.objects.all()
    serializer_class = TholaConfigSerializer

    @action(detail=True, url_path="livedata")
    def livedata(self, _, pk):
        """Read all available live data of a given device."""
        thola_config = get_object_or_404(self.queryset, pk=pk)
        if thola_config.device.primary_ip4 is None:
            raise ServiceUnavailable("No IP is set for the device " + thola_config.device.name)

        results = read_available_data(thola_config)

        if results.get('error'):
            raise ServiceUnavailable(results.get('error'))

        return Response(results)


class TholaOnboardingViews(ModelViewSet):
    """API view for thola onboarding operations."""

    queryset = TholaOnboarding.objects.all()
    serializer_class = TholaOnboardingSerializer

    @action(methods=['post'], detail=True, url_path="onboard")
    def onboard(self, _, pk):
        """Try to onboard a given onboarding task. If successful, set the status to 'success'."""
        thola_onboarding = get_object_or_404(self.queryset, pk=pk)

        queue = django_rq.get_queue('default')
        queue.enqueue("thola_nautobot.worker.onboard_device", thola_onboarding)

        # TODO
        return Response()
