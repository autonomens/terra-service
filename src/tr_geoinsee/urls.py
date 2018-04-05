from django.urls import path, include
from rest_framework import routers

from .views import StateViewSet

router = routers.SimpleRouter()

router.register(r'state', StateViewSet, base_name='state')

urlpatterns = []
urlpatterns += router.urls
