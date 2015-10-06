
{%- set app = salt['pillar.get']('horizon:server:app:'+app_name) %}


import os
import sys

sys.stdout = sys.stderr

sys.path.append('/srv/horizon/site')

import site

site.addsitedir('/srv/horizon/lib/python2.7/site-packages')

# Avoid ``[Errno 13] Permission denied: '/var/www/.python-eggs'`` messages

import os
#os.environ['PYTHON_EGG_CACHE'] = '/www/lostquery.com/mod_wsgi/egg-cache'

sys.path.append('/srv/horizon/site')
{%- if pillar.horizon.server.plugins is defined %}
{%- for plugin in pillar.horizon.server.plugins %}
sys.path.append('/srv/horizon/plugins/{{ plugin.name }}')
{%- endfor %}
{%- endif %}

os.environ['DJANGO_SETTINGS_MODULE'] = 'openstack_dashboard.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
