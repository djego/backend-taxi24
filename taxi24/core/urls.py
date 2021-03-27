from rest_framework import routers
from core.views import DriverViewSet, PassengerViewSet, TripViewSet

router = routers.DefaultRouter()
router.register(r'drivers', DriverViewSet)
router.register(r'passengers', PassengerViewSet)
router.register(r'trips', TripViewSet)

urlpatterns = router.urls