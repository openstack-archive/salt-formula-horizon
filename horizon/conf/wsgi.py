
import os
import sys

sys.stdout = sys.stderr

{%- set app = salt['pillar.get']('horizon:server:app:'+app_name) %}

import site

from os.path import join

#site.addsitedir('/srv/horizon/lib/python2.7/site-packages')

path = '/srv/horizon'

sys.path.append(join(path, 'lib', 'python2.7', 'site-packages'))
sys.path.append(join(path, 'sites', '{{ app_name }}', 'lib'))

{%- if app.plugin is defined %}
{%- for plugin_name, plugin in app.plugin.iteritems() %}
sys.path.append('/srv/horizon/sites/{{ app_name }}/plugins/{{ plugin_name }}')
{%- endfor %}
{%- endif %}

import os
#os.environ['PYTHON_EGG_CACHE'] = '/www/lostquery.com/mod_wsgi/egg-cache'

os.environ['DJANGO_SETTINGS_MODULE'] = 'openstack_dashboard.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
