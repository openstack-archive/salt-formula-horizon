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

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
    'horizon.loaders.TemplateLoader'
)

INSTALLED_APPS = (
    {%- for plugin_name, plugin in app.plugin.iteritems() %}
    '{{ plugin.app }}',
    {%- if plugin_name == 'robotice_dashboard' %}
    'robotice_dashboard.dashboards.location',
    'robotice_dashboard.dashboards.admin',
    'robotice_auth',
    {%- endif %}
    {%- if plugin_name == 'helpdesk' %}
    'redactor',
    {%- endif %}
    {%- endfor %}
    'openstack_dashboard',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'compressor',
    'horizon',
    {%- if app.version == 'csb' %}
    'markitup',
    'image_proxy',
    'csb_dashboard.dashboards.service',
    'csb_dashboard.dashboards.admin',
    'csb_dashboard.dashboards.api_office365',
    'csb_dashboard.dashboards.heat_stack',
    'csb_dashboard.dashboards.salt_cloud',
    'csb_dashboard.dashboards.salt_system',
    {%- endif %}
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
{% include "horizon/files/horizon_settings/_websso_settings.py" %}
