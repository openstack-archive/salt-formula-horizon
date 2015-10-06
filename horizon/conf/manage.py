#!/usr/bin/env python
{%- from "horizon/map.jinja" import server with context %}

import sys
import os

sys.path.append("/usr/share/openstack-dashboard") 

{# old way #}
{%- for plugin in server.get('plugins', []) %}
sys.path.append('/srv/horizon/plugins/{{ plugin.name }}')
{%- endfor %}

{# new way #}
{%- for plugin_name, plugin in server.get('plugin', {}).iteritems() %}
sys.path.append('/srv/horizon/plugins/{{ plugin_name }}')
{%- endfor %}

from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "openstack_dashboard.settings")
    execute_from_command_line(sys.argv)
