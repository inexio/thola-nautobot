"""REST API urls for thola nautobot."""
from nautobot.core.api import OrderedDefaultRouter
from . import views

router = OrderedDefaultRouter()
# router.APIRootView = None
router.register("live_data", views.ReadLiveData)
urlpatterns = router.urls

app_name = "thola-api"
