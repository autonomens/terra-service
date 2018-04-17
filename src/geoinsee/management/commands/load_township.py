from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.gdal import DataSource
import os
import logging
from geoinsee.models import AdministrativeEntity, ZIPCode

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load township from shapefiles in database"

    def add_arguments(self, parser):
        parser.add_argument('shapefile')

    def handle(self, *args, **options):
        filename = options.get('shapefile')
        if not filename:
            raise CommandError('You need to give a shapefile with this command')
        if not os.path.exists(filename):
            raise CommandError('File does not exists at: %s' % filename)
        datasource = DataSource(filename, 1)
        count = datasource.layer_count

        logger.info('%s layers found' % count)
        geometry, name, zip_code, insee_code = ([] for i in range(4))

        for layer in datasource:
            geometry.extend(layer.get_geoms(geos=True))
            name.extend(layer.get_fields("nom_comm"))
            zip_code.extend(layer.get_fields("postal_code"))
            insee_code.extend(layer.get_fields("insee_com"))

        logger.info('%s township found' % len(geometry))

        for i, geom in enumerate(geometry):
            tmp = zip_code[i]
            entity, _ = AdministrativeEntity.objects.update_or_create(geom=geom,
                                                                      name=name[i], insee=insee_code[i])
            for value in tmp.split("/"):
                ZIPCode.objects.get_or_create(zip_code=value, insee=entity)
        self.stdout.write('DONE')
