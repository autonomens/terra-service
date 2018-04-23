from rest_framework import routers

from .views import GeocodingViewset

router = routers.SimpleRouter()

router.register(r'', GeocodingViewset, base_name='geocoding')

urlpatterns = router.urls
