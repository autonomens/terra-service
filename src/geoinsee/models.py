from django.contrib.gis.db import models
from django.conf import settings
# Create your models here.


class AdministrativeEntity(models.Model):
    name = models.CharField(blank=False, max_length=163, help_text='Administrative Entity name')
    insee = models.CharField(max_length=5, blank=False, unique=True, help_text='Insee Code')
    geom = models.GeometryField(dim=2, srid=settings.SRID, spatial_index=False, editable=False, null=False, default=None)


class ZIPCode(models.Model):
    insee = models.ForeignKey(AdministrativeEntity, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=5, blank=False, unique=False, help_text='Zip Code')