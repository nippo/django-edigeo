#-*- coding: utf-8 -*-
import os
import tarfile
import shutil
import tempfile
import hashlib
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.gdal import DataSource
from edigeo.models import EdigeoSection
from edigeo.models import EdigeoLieuDit
from edigeo.models import EdigeoParcelle
from edigeo.models import EdigeoSubdFisc
from edigeo.models import EdigeoBorneParcel
from edigeo.models import EdigeoBati
from edigeo.models import EdigeoCommune
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
            s.idu = f['idu'].value
            s.tex = f['tex'].value
            try:
                s.the_geom = GEOSGeometry(f.geom.geojson, srid=27563)
                s.save()
            except IntegrityError:
                self.stdout.write('  Section %s is already in DB!' % f['idu'])
            except:
                self.stderr.write(
                    '  A problem occured with section %s!' % f['idu'])

    def save_lieu_dit(self, layer):
        for f in layer:
            s = EdigeoLieuDit()
            s.tex = f['tex'].value.upper()
            s.md5 = hashlib.sha224(f.geom.geojson).hexdigest()
            try:
                s.the_geom = GEOSGeometry(f.geom.geojson, srid=27563)
                s.save()
            except IntegrityError:
                self.stdout.write(
                    '  Lieu-dit %s is already in DB!' % f['tex'])
            except:
                self.stderr.write(
                    '  A problem occured with lieudit %s!' % f['tex'])

    def save_parcelle(self, layer):
        for f in layer:
            s = EdigeoParcelle()
            s.idu = f['idu'].value
            s.supf = f['supf'].value
            s.tex = f['tex'].value
            s.commune_idu = f['idu'].value[:3]
            s.section_idu = f['idu'].value[:8]
            try:
                s.the_geom = GEOSGeometry(f.geom.geojson, srid=27563)
                s.save()
            except IntegrityError:
                EdigeoParcelle.objects.filter(idu=f['idu']).update(
                    commune_idu=f['idu'].value[:3],
                    section_idu=f['idu'].value[:8]
                )
            except:
                self.stderr.write(
                    '  A problem occured with parcelle %s!' % f['idu'])

    def save_subd_fisc(self, layer):
        for f in layer:
            s = EdigeoSubdFisc()
            s.tex = f['tex'].value
            s.md5 = hashlib.sha224(f.geom.geojson).hexdigest()
            try:
                s.the_geom = GEOSGeometry(f.geom.geojson, srid=27563)
                s.save()
            except IntegrityError:
                self.stdout.write(
                    '  Subfisc %s is already in DB!' % f['tex'])
            except:
                self.stderr.write(
                    '  A problem occured with sub_fisc %s!' % f['tex'])

    def save_borne_parcel(self, layer):
        for f in layer:
            s = EdigeoBorneParcel()
            s.md5 = hashlib.sha224(f.geom.geojson).hexdigest()
            try:
                s.the_geom = GEOSGeometry(f.geom.geojson, srid=27563)
                s.save()
            except IntegrityError:
                self.stdout.write('  BorneParcel is already in DB!')
            except:
                self.stderr.write('  A problem occured with borne_parcel!')

    def save_bati(self, layer):
        for f in layer:
            s = EdigeoBati()
            s.md5 = hashlib.sha224(f.geom.geojson).hexdigest()
            try:
                s.the_geom = GEOSGeometry(f.geom.geojson, srid=27563)
                s.save()
            except IntegrityError:
                self.stdout.write('  This bati is already in DB!')
            except:
                self.stderr.write('  A problem occured with this bati!')

    def save_commune(self, layer):
        for f in layer:
            s = EdigeoCommune()
            s.idu = f['idu'].value
            s.gb_ident = f['gb_ident'].value
            try:
                s.the_geom = GEOSGeometry(f.geom.geojson, srid=27563)
                s.save()
            except IntegrityError:
                self.stdout.write(
                    '  Commune %s is already in DB!' % f['idu'])
            except:
                self.stderr.write(
                    '  A problem occured with this commune %s!' % f['idu'])

    def do_it_or_not(self, layer):
        if layer.name == 'PARCELLE':
            self.save_parcelle(layer)
        #if layer.name == 'SECTION':
            #self.save_section(layer)
        #elif layer.name == 'LIEU_DIT':
            #self.save_lieu_dit(layer)
        #elif layer.name == 'PARCELLE':
            #self.save_parcelle(layer)
        #elif layer.name == 'SUBD_FISC':
            #self.save_subd_fisc(layer)
        #elif layer.name == 'BORNE_PARCEL':
            #self.save_borne_parcel(layer)
        #elif layer.name == 'BATI':
            #self.save_bati(layer)
        #elif layer.name == 'COMMUNE':
            #self.save_commune(layer)

    def handle(self, *args, **options):
        sections_path = self.get_sections_path(args)
        self.init_dirs()
        for path, dirname, files in os.walk(sections_path):
            if len(files) == 0:
                continue
            self.generate_mif(path, files)
            section = DataSource(os.path.join(tempfile.gettempdir(), 'mif'))
            for layer in section:
                self.do_it_or_not(layer)
            self.init_dirs()
