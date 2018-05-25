from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.gdal import DataSource
import os
import logging
from geoinsee.models import AdministrativeEntity, ZIPCode

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load states from shapefiles in database"

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
        geometry, name, insee_code = ([] for i in range(3))

        for layer in datasource:
            geometry.extend(layer.get_geoms(geos=True))
            name.extend(layer.get_fields('nom'))
            insee_code.extend(layer.get_fields('code_insee'))

        logger.info('%s states found' % len(geometry))

        for i, geom in enumerate(geometry):
            entity, _ = AdministrativeEntity.objects.update_or_create(geom=geom,
                                                                      name=name[i], insee=insee_code[i])
        self.stdout.write('DONE')
