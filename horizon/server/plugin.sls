{%- from "horizon/map.jinja" import server with context %}
{%- if server.enabled %}

{%- for plugin_name, plugin in server.get('plugin', {}).iteritems() %}

horizon_{{ plugin_name }}_package:
  pkg.installed:
  - name: {{ plugin.source.name }}
  - watch_in:
    - service: horizon_services
  {%- if grains.os == "Ubuntu" %}
  - require:
    - pkg: horizon_ubuntu_theme_absent
  {%- endif %}

{%- endfor %}

{%- if grains.os == "Ubuntu" %}

horizon_ubuntu_theme_absent:
  pkg.purged:
  - name: openstack-dashboard-ubuntu-theme

{%- endif %}

{%- endif %}