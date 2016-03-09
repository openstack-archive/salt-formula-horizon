import os
from django.utils.translation import ugettext_lazy as _
from openstack_dashboard import exceptions

{%- from "horizon/map.jinja" import server with context %}

{%- if server.app is defined %}
{%- set app = salt['pillar.get']('horizon:server:app:'+app_name) %}
{%- else %}
{%- set app = salt['pillar.get']('horizon:server') %}
{%- endif %}

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
    'password_autocomplete': 'on'
}

SESSION_TIMEOUT = 3600 * 24

{%- if app.theme is defined or app.plugin.horizon_theme is defined %}
{%- if app.theme is defined %}
CUSTOM_THEME_PATH = 'dashboards/theme/static/themes/{{ app.theme }}'
{%- elif app.plugin.horizon_theme.theme_name is defined %}
# Enable custom theme if it is present.
try:
  from openstack_dashboard.enabled._99_horizon_theme import CUSTOM_THEME_PATH
except ImportError:
  pass
{%- endif %}
{%- endif %}

INSTALLED_APPS = (
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

{% include "horizon/files/horizon_settings/_keystone_settings.py" %}
{% include "horizon/files/horizon_settings/_local_settings.py" %}

AUTHENTICATION_BACKENDS = ('helpdesk_auth.backend.HelpdeskBackend',)

AUTHENTICATION_URLS = ['helpdesk_auth.urls']

API_RESULT_PAGE_SIZE = 25

{% include "horizon/files/horizon_settings/_horizon_settings.py" %}

