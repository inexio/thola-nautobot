"""REST API urls for thola nautobot."""
from nautobot.core.api import OrderedDefaultRouter
from .views import TholaDeviceViews

router = OrderedDefaultRouter()
router.register("tholadevice", TholaDeviceViews)

urlpatterns = router.urls
