# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Event'
        db.create_table('core_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('performer', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('performer_links', self.gf('tinymce.models.HTMLField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=40, db_index=True)),
            ('press_release', self.gf('tinymce.models.HTMLField')()),
            ('map', self.gf('tinymce.models.HTMLField')()),
            ('stage_address', self.gf('tinymce.models.HTMLField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('core', ['Event'])

        # Adding model 'Client'
        db.create_table('core_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('phone', self.gf('phonenumber_field.modelfields.PhoneNumberField')(max_length=128)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Event'])),
        ))
        db.send_create_signal('core', ['Client'])

        # Adding model 'PriceCategory'
        db.create_table('core_pricecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('price', self.gf('django.db.models.fields.IntegerField')()),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Event'])),
        ))
        db.send_create_signal('core', ['PriceCategory'])

        # Adding model 'Stage'
        db.create_table('core_stage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stages', to=orm['core.Event'])),
        ))
        db.send_create_signal('core', ['Stage'])

        # Adding model 'Placement'
        db.create_table('core_placement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('stage', self.gf('django.db.models.fields.related.ForeignKey')(related_name='placements', to=orm['core.Stage'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Event'])),
        ))
        db.send_create_signal('core', ['Placement'])

        # Adding model 'Row'
        db.create_table('core_row', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('placement', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rows', to=orm['core.Placement'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Event'])),
        ))
        db.send_create_signal('core', ['Row'])

        # Adding model 'Tag'
        db.create_table('core_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tags', to=orm['core.Event'])),
        ))
        db.send_create_signal('core', ['Tag'])

        # Adding model 'Order'
        db.create_table('core_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orders', to=orm['core.Client'])),
            ('status', self.gf('django.db.models.fields.CharField')(default=('R', 'Running'), max_length=1)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('close_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orders', to=orm['core.Event'])),
        ))
        db.send_create_signal('core', ['Order'])

        # Adding model 'Seat'
        db.create_table('core_seat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='F', max_length=1)),
            ('price_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.PriceCategory'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='seats', null=True, to=orm['core.Tag'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('row', self.gf('django.db.models.fields.related.ForeignKey')(related_name='seats', to=orm['core.Row'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='seats', null=True, to=orm['core.Order'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='seats', to=orm['core.Event'])),
        ))
        db.send_create_signal('core', ['Seat'])

        # Adding model 'UserProfile'
        db.create_table('core_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='profiles', null=True, to=orm['core.Event'])),
        ))
        db.send_create_signal('core', ['UserProfile'])


    def backwards(self, orm):
        
        # Deleting model 'Event'
        db.delete_table('core_event')

        # Deleting model 'Client'
        db.delete_table('core_client')

        # Deleting model 'PriceCategory'
        db.delete_table('core_pricecategory')

        # Deleting model 'Stage'
        db.delete_table('core_stage')

        # Deleting model 'Placement'
        db.delete_table('core_placement')

        # Deleting model 'Row'
        db.delete_table('core_row')

        # Deleting model 'Tag'
        db.delete_table('core_tag')

        # Deleting model 'Order'
        db.delete_table('core_order')

        # Deleting model 'Seat'
        db.delete_table('core_seat')

        # Deleting model 'UserProfile'
        db.delete_table('core_userprofile')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.client': {
            'Meta': {'object_name': 'Client'},
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('phonenumber_field.modelfields.PhoneNumberField', [], {'max_length': '128'})
        },
        'core.event': {
            'Meta': {'object_name': 'Event'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map': ('tinymce.models.HTMLField', [], {}),
            'performer': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'performer_links': ('tinymce.models.HTMLField', [], {}),
            'press_release': ('tinymce.models.HTMLField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40', 'db_index': 'True'}),
            'stage_address': ('tinymce.models.HTMLField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.order': {
            'Meta': {'object_name': 'Order'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['core.Client']"}),
            'close_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['core.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "('R', 'Running')", 'max_length': '1'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        'core.placement': {
            'Meta': {'object_name': 'Placement'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'placements'", 'to': "orm['core.Stage']"})
        },
        'core.pricecategory': {
            'Meta': {'object_name': 'PriceCategory'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {})
        },
        'core.row': {
            'Meta': {'object_name': 'Row'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'placement': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': "orm['core.Placement']"})
        },
        'core.seat': {
            'Meta': {'object_name': 'Seat'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'seats'", 'to': "orm['core.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'seats'", 'null': 'True', 'to': "orm['core.Order']"}),
            'price_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.PriceCategory']"}),
            'row': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'seats'", 'to': "orm['core.Row']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'F'", 'max_length': '1'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'seats'", 'null': 'True', 'to': "orm['core.Tag']"})
        },
        'core.stage': {
            'Meta': {'object_name': 'Stage'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stages'", 'to': "orm['core.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.tag': {
            'Meta': {'object_name': 'Tag'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tags'", 'to': "orm['core.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'profiles'", 'null': 'True', 'to': "orm['core.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['core']
