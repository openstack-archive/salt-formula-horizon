import os
from django.utils.translation import ugettext_lazy as _
from openstack_dashboard import exceptions

{%- from "horizon/map.jinja" import server with context %}
{%- set app = salt['pillar.get']('horizon:server:app:'+app_name) %}

# OpenStack Dashboard configuration.
HORIZON_CONFIG = {
    'dashboards': ({% if app.plugin is defined %}{% for plugin_name, plugin in app.plugin.iteritems() %}{% if plugin.get('dashboard', False) %}'{{ plugin_name }}', {% endif %}{% endfor %}{% endif %}'admin', 'settings'),
    'default_dashboard': '{{ app.get('default_dashboard', 'project') }}',
    'user_home': 'helpdesk_dashboard.views.splash',
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
    {%- if not plugin_name == 'horizon_theme' %}
    '{{ plugin.app }}',
    {%- endif %}
    {%- endfor %}
    'helpdesk_auth',
    'redactor',
    'openstack_dashboard',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'compressor',
    'horizon',
    {%- if app.logging is defined %}
    'raven.contrib.django.raven_compat',
    {%- endif %}
)

REDACTOR_OPTIONS = {'lang': 'en', 'buttonsHide': ['file', 'image']}
REDACTOR_UPLOAD = 'uploads/'

ROOT_URLCONF = 'helpdesk_dashboard.url_overrides'

AUTHENTICATION_BACKENDS = ('helpdesk_auth.backend.HelpdeskBackend',)

AUTHENTICATION_URLS = ['helpdesk_auth.urls']

{% include "horizon/files/horizon_settings/_local_settings.py" %}
{% include "horizon/files/horizon_settings/_horizon_settings.py" %}
{% include "horizon/files/horizon_settings/_keystone_settings.py" %}
