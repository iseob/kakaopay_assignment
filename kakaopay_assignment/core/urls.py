from rest_framework_nested import routers
from devices.views import DevicesViewSet
from stats.views import StatsViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'devices', DevicesViewSet)
router.register(r'stats', StatsViewSet)

urlpatterns = router.urls
