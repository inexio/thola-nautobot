"""REST API urls for thola nautobot."""
from nautobot.core.api import OrderedDefaultRouter
from .views import TholaConfigViews

router = OrderedDefaultRouter()
router.register("config", TholaConfigViews)

urlpatterns = router.urls
