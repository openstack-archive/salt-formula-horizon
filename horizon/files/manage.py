#!/usr/bin/env python
{%- set app = salt['pillar.get']('horizon:server:app:'+app_name) %}

import sys
import os

from os.path import join

path = '/srv/horizon'

sys.path.append(join(path, 'sites', '{{ app_name }}', 'lib', 'python2.7', 'site-packages'))
sys.path.append(join(path, 'sites', '{{ app_name }}', 'extra'))
{%- if app.plugin is defined %}
{%- for plugin_name, plugin in app.plugin.iteritems() %}
sys.path.append(join(path, 'sites', '{{ app_name }}', 'plugins', '{{ plugin_name }}'))
{%- endfor %}
{%- endif %}

from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ app.get('dashboard', 'openstack') }}_dashboard.settings")
    execute_from_command_line(sys.argv)
