import os
from django.utils.translation import ugettext_lazy as _
from openstack_dashboard import exceptions

{%- from "horizon/map.jinja" import server with context %}
{%- set app = salt['pillar.get']('horizon:server:app:'+app_name) %}

HORIZON_CONFIG = {
    'dashboards': ({% if app.plugin is defined %}{% for plugin_name, plugin in app.plugin.iteritems() %}{% if plugin.get('dashboard', False) %}'{{ plugin_name }}', {% endif %}{% endfor %}{% endif %}'admin', 'settings'),
    'default_dashboard': '{{ app.get('default_dashboard', 'project') }}',
    'user_home': '{{ app.get('user_home', 'openstack_dashboard.views.get_user_home') }}',
    'ajax_queue_limit': 10,
    'auto_fade_alerts': {
        'delay': 3000,
        'fade_duration': 1500,
        'types': ['alert-success', 'alert-info']
    },
    'help_url': "{{ app.get('help_url', 'http://docs.openstack.org') }}",
    'exceptions': {'recoverable': exceptions.RECOVERABLE,
                   'not_found': exceptions.NOT_FOUND,
                   'unauthorized': exceptions.UNAUTHORIZED},
}

INSTALLED_APPS = (
    {%- for plugin_name, plugin in app.plugin.iteritems() %}
    '{{ plugin.app }}',
    {%- endfor %}
    'csb_dashboard',
    'csb_dashboard.dashboards.service',
    'csb_dashboard.dashboards.admin',
    'csb_dashboard.dashboards.api_office365',
    'csb_dashboard.dashboards.heat_stack',
    'csb_dashboard.dashboards.salt_cloud',
    'csb_dashboard.dashboards.salt_system',
    'theme',
    'horizon_overrides',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'compressor',
    'horizon',
    'csbclient',
    'csb_auth',
    'markitup',
    'image_proxy',
    {%- if app.logging is defined %}
    'raven.contrib.django.raven_compat',
    {%- endif %}
)

MEDIA_ROOT = '/srv/horizon/sites/{{ app_name }}/media/'
STATIC_ROOT = '/srv/horizon/sites/{{ app_name }}/static/'

{% include "horizon/files/horizon_settings/_local_settings.py" %}