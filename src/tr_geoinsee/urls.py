from django.urls import path, include
from rest_framework import routers

from .views import StateViewSet, CountyViewSet, TownshipViewset

router = routers.SimpleRouter()

router.register(r'state', StateViewSet, base_name='state')
router.register(r'county', CountyViewSet, base_name='county')
router.register(r'township', TownshipViewset, base_name='township')


urlpatterns = []
urlpatterns += router.urls
