#-*- coding: utf-8 -*-
import os
import tarfile
import shutil
import tempfile
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.gdal import DataSource
from edigeo.models import EdigeoSection
from django.contrib.gis.geos import GEOSGeometry
from django.db.utils import IntegrityError


class Command(BaseCommand):
    args = '<tar_path>'
    help = 'Load EDIGEO data for the specified tables'

    def get_sections_path(self, args):

        if len(args) == 0:
            raise CommandError('We need a directory as argument!')

        for arg in args:
            sections_path = os.path.join(arg)
            if not os.path.exists(os.path.join(sections_path)):
                raise CommandError('Invalid path!')

        return sections_path

    def init_dirs(self):

        for d in ['mif', 'in', 'log']:
            if os.path.exists(os.path.join(tempfile.gettempdir(), d)):
                shutil.rmtree(os.path.join(tempfile.gettempdir(), d))
            os.makedirs(os.path.join(tempfile.gettempdir(), d))

    def generate_mif(self, path, files):
        tar = tarfile.open(os.path.join(path, files.pop()))
        tar.extractall(os.path.join(tempfile.gettempdir(), 'in'))
        os.system('perl %s/edi2mif.pl %s %s > %s/tmp.log' % (
            os.path.dirname(os.path.realpath(__file__)),
            os.path.join(tempfile.gettempdir(), 'in'),
            os.path.join(tempfile.gettempdir(), 'mif'),
            os.path.join(tempfile.gettempdir(), 'log'),
        ))

    def save_section(self, layer):
        for f in layer:
            s = EdigeoSection()
            s.gb_ident = f['gb_ident'].value
            s.idu = f['idu'].value
            s.tex = f['tex'].value
            try:
                s.the_geom = GEOSGeometry(f.geom.geojson, srid=27563)
                s.save()
            except IntegrityError:
                self.stdout.write('Section %s is already in DB!' % f['idu'])
            except:
                self.stderr.write('A problem occured with section %s!' % f['idu'])


    def handle(self, *args, **options):
        sections_path = self.get_sections_path(args)
        self.init_dirs()
        for path, dirname, files in os.walk(sections_path):
            if len(files) == 0:
                continue
            self.generate_mif(path, files)
            section = DataSource(os.path.join(tempfile.gettempdir(), 'mif'))
            for layer in section:
                if layer.name == 'SECTION':
                    self.save_section(layer)
            self.init_dirs()
