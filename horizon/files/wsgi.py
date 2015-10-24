
import os
import sys

sys.stdout = sys.stderr

{%- set app = salt['pillar.get']('horizon:server:app:'+app_name) %}

import site

from os.path import join

#site.addsitedir('/srv/horizon/lib/python2.7/site-packages')

path = '/srv/horizon'

sys.path.append(join(path, 'sites', '{{ app_name }}', 'lib', 'python2.7', 'site-packages'))
sys.path.append(join(path, 'sites', '{{ app_name }}', 'extra'))
{%- if app.plugin is defined %}
{%- for plugin_name, plugin in app.plugin.iteritems() %}
sys.path.append(join(path, 'sites', '{{ app_name }}', 'plugins', '{{ plugin_name }}'))
{%- endfor %}
{%- endif %}

import os
#os.environ['PYTHON_EGG_CACHE'] = '/www/lostquery.com/mod_wsgi/egg-cache'

os.environ['DJANGO_SETTINGS_MODULE'] = '{{ app.get('dashboard', 'openstack') }}_dashboard.settings'

import django
if django.VERSION < (1, 6):
    from django.core.handlers.wsgi import WSGIHandler

    application = WSGIHandler()
else:
    # From 1.4 wsgi support was improved and since 1.7 old style WSGI script
    # causes AppRegistryNotReady exception
    # https://docs.djangoproject.com/en/dev/releases/1.7/#wsgi-scripts
    from django.core.wsgi import get_wsgi_application

    application = get_wsgi_application()
