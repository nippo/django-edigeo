#-*- coding: utf-8 -*-
import os
import tarfile
import shutil
import tempfile
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping
from edigeo.models import EdigeoLieuDit
from edigeo.models import edigeolieudit_mapping


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

    def handle(self, *args, **options):

        self.init_dirs()
        sections_path = self.get_sections_path(args)
        for path, dirname, files in os.walk(sections_path):
            if len(files) == 0:
                continue
            self.generate_mif(path, files)
            section = DataSource(os.path.join(tempfile.gettempdir(), 'mif'))
            for layer in section:
                if layer.name == 'LIEU_DIT':
                    import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
                    lm = LayerMapping(
                        EdigeoLieuDit,
                        layer,
                        edigeolieudit_mapping,
                        transform=True,
                        encoding='UTF-8'
                    )
                    print layer
                            #insert_in_edigeo_tmp(layer)
                            #update_table_for_layer(layer)
                            #for d in ['shp', 'mif', 'in']:
                                #shutil.rmtree(d)
                                #os.makedirs(d)

    def convert_to_shape(layer):
        os.system(('ogr2ogr -f "ESRI Shapefile" \
                -t_srs "EPSG:4326" \
                -s_srs "EPSG:27563" \
                -a_srs "EPSG:3857" \
                shp/{0}.shp mif/{0}.MIF').format(layer))

    def insert_in_edigeo_tmp(name):
        os.system('psql edigeo -c "drop table if exists\
                  edigeo_tmp;" > /dev/null')
        os.system(('shp2pgsql -s 3857 -g the_geom -c \
                shp/{0}.shp edigeo_tmp edigeo  \
                | psql -d edigeo > /dev/null').format(name))

    def update_table_for_layer(name):
        pass
        #conn = psycopg2.connect(
            #"dbname='edigeo' user='nicolas' host='localhost' \
            #password='1Terestedin;'")
        #cur = conn.cursor()
        #cur.execute('select * from information_schema.tables where \
            #table_name=\'edigeo_' + name.lower() + '\'')
        # If table does not exist
        #if cur.rowcount == 0:
            #os.system(('psql edigeo -c "create table \
                    #edigeo_{0} as select * from edigeo_tmp \
                    #with no data;" > /dev/null').format(name))
            #os.system(('psql edigeo -c "alter table edigeo_{0} \
                    #add constraint constraint_name unique(idu)";'
            #).format(name))
        #else:
            #os.system(('psql edigeo -c "update edigeo_tmp set \
                    #gid=gid+(select max(gid) from edigeo_{0});"'
            #).format(name))
        #os.system(('psql edigeo -c "insert into edigeo_{0} select * \
            # from edigeo_tmp;"').format(name))
