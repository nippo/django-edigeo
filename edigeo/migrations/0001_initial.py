# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        pass

    def backwards(self, orm):
        # Deleting model 'EdigeoBati'
        db.delete_table(u'edigeo_bati')

        # Deleting model 'EdigeoBorneParcel'
        db.delete_table(u'edigeo_borne_parcel')

        # Deleting model 'EdigeoLieuDit'
        db.delete_table(u'edigeo_lieu_dit')

        # Deleting model 'Parcelle'
        db.delete_table(u'edigeo_parcelle')

        # Deleting model 'EdigeoSubdFisc'
        db.delete_table(u'edigeo_subd_fisc')

    models = {
        u'edigeo.edigeobati': {
            'Meta': {'object_name': 'EdigeoBati', 'db_table': "u'edigeo_bati'"},
            'dur': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'gb_ident': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'gb_idnum': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'the_geom': ('django.contrib.gis.db.models.fields.GeometryField', [], {'null': 'True', 'blank': 'True'})
        },
        u'edigeo.edigeoborneparcel': {
            'Meta': {'object_name': 'EdigeoBorneParcel', 'db_table': "u'edigeo_borne_parcel'"},
            'gb_ident': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'gb_idnum': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'the_geom': ('django.contrib.gis.db.models.fields.GeometryField', [], {'null': 'True', 'blank': 'True'})
        },
        u'edigeo.edigeolieudit': {
            'Meta': {'object_name': 'EdigeoLieuDit', 'db_table': "u'edigeo_lieu_dit'"},
            'gb_ident': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'gb_idnum': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'tex': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'tex10': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'tex2': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'tex3': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'tex4': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'tex5': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'tex6': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'tex7': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'tex8': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'tex9': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'the_geom': ('django.contrib.gis.db.models.fields.GeometryField', [], {'null': 'True', 'blank': 'True'})
        },
        u'edigeo.edigeosubdfisc': {
            'Meta': {'object_name': 'EdigeoSubdFisc', 'db_table': "u'edigeo_subd_fisc'"},
            'gb_ident': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'gb_idnum': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'tex': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'the_geom': ('django.contrib.gis.db.models.fields.GeometryField', [], {'null': 'True', 'blank': 'True'})
        },
        u'edigeo.parcelle': {
            'Meta': {'object_name': 'Parcelle'},
            'coar': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'codm': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'gb_ident': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'gb_idnum': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'idu': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'indp': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'supf': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '65535', 'decimal_places': '65535', 'blank': 'True'}),
            'tex': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'tex2': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'the_geom': ('django.contrib.gis.db.models.fields.GeometryField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['edigeo']
