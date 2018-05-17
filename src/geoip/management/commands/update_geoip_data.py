import os
import tarfile
import tempfile
import shutil

import requests

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Download GEOIP files from maxmind servers to GEOIP_PATH"
    base_url = 'http://geolite.maxmind.com/download/geoip/database/'
    files = ['GeoLite2-City.tar.gz', 'GeoLite2-Country.tar.gz']

    def handle(self, *args, **options):
        if not hasattr(settings, 'GEOIP_PATH'):
            raise Exception('GEOIP_PATH is not defined')

        if not os.path.exists(settings.GEOIP_PATH):
            raise Exception('GEOIP_PATH folder does not exist')

        self.stdout.write(f'Updating GeoIP2 database files')

        for filename in self.files:
            file_url = f"{self.base_url}{filename}"
            self.stdout.write(f'Loading {file_url}')
            r = requests.get(file_url, stream=True)
            
            if r.status_code == 200:
                with tempfile.NamedTemporaryFile() as tmp_file:
                    tmp_file.write(r.raw.read())
                    tmp_file.seek(0)

                    with tarfile.open(fileobj=tmp_file, mode='r:gz') as geoip_file:
                        for member in geoip_file.getmembers():
                            if os.path.splitext(member.path)[1] == '.mmdb':
                                member.path = os.path.basename(member.path)
                                geoip_file.extract(member, settings.GEOIP_PATH)
                    
                                self.stdout.write(f"{member.path} is now up to date")