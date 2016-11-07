import os
from django.utils.translation import ugettext_lazy as _
from openstack_dashboard import exceptions

{%- from "horizon/map.jinja" import server with context %}

{%- if server.app is defined %}
{%- set app = salt['pillar.get']('horizon:server:app:'+app_name) %}
{%- else %}
{%- set app = salt['pillar.get']('horizon:server') %}
{%- endif %}

HORIZON_CONFIG = {
    'user_home': 'openstack_dashboard.views.get_user_home',
    'ajax_queue_limit': 10,
    'auto_fade_alerts': {
        'delay': 3000,
        'fade_duration': 1500,
        'types': ['alert-success', 'alert-info']
    },
    'help_url': "http://docs.openstack.org",
    'exceptions': {'recoverable': exceptions.RECOVERABLE,
                   'not_found': exceptions.NOT_FOUND,
                   'unauthorized': exceptions.UNAUTHORIZED},
    'modal_backdrop': 'static',
    'angular_modules': [],
    'js_files': [],
    'js_spec_files': [],
    'password_autocomplete': 'on'
}

{%- if app.theme is defined %}
CUSTOM_THEME_PATH = 'static/themes/{{ app.theme }}'
{%- elif app.plugin is defined and app.plugin.horizon_theme.theme_name is defined %}
CUSTOM_THEME_PATH = 'static/themes/{{ app.plugin.horizon_theme.theme_name }}'
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
    'openstack_auth',
    {%- if app.logging is defined %}
    'raven.contrib.django.raven_compat',
    {%- endif %}
)

{% include "horizon/files/horizon_settings/_local_settings.py" %}
{% include "horizon/files/horizon_settings/_horizon_settings.py" %}
{% include "horizon/files/horizon_settings/_keystone_settings.py" %}
{% include "horizon/files/horizon_settings/_nova_settings.py" %}
{% include "horizon/files/horizon_settings/_glance_settings.py" %}
{% include "horizon/files/horizon_settings/_neutron_settings.py" %}
