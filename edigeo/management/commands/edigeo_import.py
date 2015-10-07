# -*- coding: utf-8 -*-
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from edigeo.models import EdigeoBati
from edigeo.models import EdigeoBorneParcel
from edigeo.models import EdigeoCommune
from edigeo.models import EdigeoLieuDit
from edigeo.models import EdigeoParcelle
from edigeo.models import EdigeoSection
from edigeo.models import EdigeoSubdFisc
import hashlib
import os
import shutil
import tarfile
import tempfile


class Command(BaseCommand):
    args = '<tar_path>'
    help = 'Load EDIGEO data from specifified dir'

    def add_arguments(self, parser):
        parser.add_argument('--path')
        parser.add_argument('--layers', default='COMMUNE SECTION LIEU_DIT PARCELLE SUBD_FISC BATI BORNE_PARCEL')  # NOQA

        # Autres commandes = 2154
        # Commande 0 27563
        parser.add_argument('--epsg', default=2154)

    def init_dirs(self):
        for d in ['mif', 'in', 'log']:
            if os.path.exists(os.path.join(tempfile.gettempdir(), d)):
                shutil.rmtree(os.path.join(tempfile.gettempdir(), d))
            os.makedirs(os.path.join(tempfile.gettempdir(), d))
            self.stderr.write('%s created!' % d)

    def generate_mif(self, path, files):
        tar = tarfile.open(os.path.join(path, files.pop()))
        tar.extractall(os.path.join(tempfile.gettempdir(), 'in'))
        os.system('perl %s/edi2mif.pl %s %s > %s/tmp.log' % (
            os.path.dirname(os.path.realpath(__file__)),
            os.path.join(tempfile.gettempdir(), 'in'),
            os.path.join(tempfile.gettempdir(), 'mif'),
            os.path.join(tempfile.gettempdir(), 'log'),
        ))

    def save_borne_parcel(self, layer):
        for f in layer:
            s = EdigeoBorneParcel()
            s.md5 = hashlib.sha224(f.geom.geojson).hexdigest()
            try:
                s.the_geom = GEOSGeometry(f.geom.geojson, srid=self.epsg)
                s.save()
            except IntegrityError:
                self.stdout.write('  BORNE_PARCEL is already in DB!')
            except:
                self.stderr.write('  A problem occured with BORNE_PARCEL!')

    def save_bati(self, layer):
        for f in layer:
            s = EdigeoBati()
            s.md5 = hashlib.sha224(f.geom.geojson).hexdigest()
            try:
                s.the_geom = GEOSGeometry(f.geom.geojson, srid=self.epsg)
                s.save()
            except IntegrityError:
                self.stdout.write('  This BATI is already in DB!')
            except:
                self.stderr.write('  A problem occured with this BATI!')

    def save_subd_fisc(self, layer):
        for f in layer:
            s = EdigeoSubdFisc()
            s.tex = f['tex'].value
            s.md5 = hashlib.sha224(f.geom.geojson).hexdigest()
            try:
                s.the_geom = GEOSGeometry(f.geom.geojson, srid=self.epsg)
                s.save()
            except IntegrityError:
                self.stdout.write(
                    '  SUBD_FISC %s is already in DB!' % f['tex'])
            except:
                self.stderr.write(
                    '  A problem occured with SUBD_FISC  %s!' % f['tex'])

    def save_parcelle(self, layer):
        for f in layer:
            s = EdigeoParcelle()
            s.idu = f['idu'].value
            s.supf = f['supf'].value
            s.tex = f['tex'].value
            s.commune_idu = f['idu'].value[:3]
            s.section_idu = f['idu'].value[:8]
            try:
                s.the_geom = GEOSGeometry(f.geom.geojson, srid=self.epsg)
                s.save()
            except IntegrityError:
                EdigeoParcelle.objects.filter(idu=f['idu']).update(
                    commune_idu=f['idu'].value[:3],
                    section_idu=f['idu'].value[:8]
                )
                self.stdout.write(
                    '  PARCELLE %s is already in DB but updated!' % f['idu'])
            except:
                self.stderr.write(
                    '  A problem occured with PARCELLE %s!' % f['idu'])

    def save_lieu_dit(self, layer):
        for f in layer:
            s = EdigeoLieuDit()
            s.tex = f['tex'].value.upper()
            s.md5 = hashlib.sha224(f.geom.geojson).hexdigest()
            try:
                s.the_geom = GEOSGeometry(f.geom.geojson, srid=self.epsg)
                s.save()
            except IntegrityError:
                self.stdout.write(
                    '  LIEU_DIT %s is already in DB!' % f['tex'])
            except:
                self.stderr.write(
                    '  A problem occured with LIEU_DIT %s!' % f['tex'])

    def save_section(self, layer):
        for f in layer:
            s = EdigeoSection()
            s.idu = f['idu'].value
            s.tex = f['tex'].value
            try:
                s.the_geom = GEOSGeometry(f.geom.geojson, srid=self.epsg)
                s.save()
            except IntegrityError:
                self.stdout.write('  SECTION %s is already in DB!' % f['idu'])
            except:
                self.stderr.write(
                    '  A problem occured with SECTION %s!' % f['idu'])

    def save_commune(self, layer):
        for f in layer:
            e = EdigeoCommune()
            e.idu = f['idu'].value
            e.gb_ident = f['gb_ident'].value
            the_geom = GEOSGeometry(f.geom.geojson, srid=self.epsg)
            the_geom.transform(3857)
            try:
                e.the_geom = the_geom
                e.save()
            except IntegrityError:
                EdigeoCommune.objects.filter(gb_ident=f['gb_ident']).update(
                    idu=f['idu'].value,
                    gb_ident=f['gb_ident'].value,
                    the_geom=the_geom
                )
                self.stdout.write(
                    '  COMMUNE %s already was in DB!' % f['idu'])
            except:
                self.stderr.write(
                    '  A problem occured with this COMMUNE %s!' % f['idu'])

    def update_db(self, layer, options):
        for opt in options.split(' '):
            if layer.name == opt:
                if opt == 'BORNE_PARCEL':
                    self.save_borne_parcel(layer)
                if opt == 'BATI':
                    self.save_bati(layer)
                if opt == 'SUBD_FISC':
                    self.save_subd_fisc(layer)
                if opt == 'PARCELLE':
                    self.save_parcelle(layer)
                if opt == 'LIEU_DIT':
                    self.save_lieu_dit(layer)
                if opt == 'SECTION':
                    self.save_section(layer)
                if opt == 'COMMUNE':
                    self.save_commune(layer)

    def handle(self, *args, **options):
        self.epsg = int(options['epsg'])

        sections_path = options['path']
        if not os.path.exists(sections_path):
            raise CommandError('Invalid path!')

        self.init_dirs()

        for path, dirname, files in os.walk(sections_path):
            if len(files) == 0:
                continue
            self.generate_mif(path, files)
            section = DataSource(os.path.join(tempfile.gettempdir(), 'mif'))
            for layer in section:
                for imported_layer in options['layers'].split(' '):
                    self.update_db(layer, imported_layer)
            self.init_dirs()
