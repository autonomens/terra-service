from django.urls import path, include
from rest_framework import routers

from .views import StateViewSet, CountyViewSet

router = routers.SimpleRouter()

router.register(r'state', StateViewSet, base_name='state')
router.register(r'county', CountyViewSet, base_name='county')


urlpatterns = []
urlpatterns += router.urls
