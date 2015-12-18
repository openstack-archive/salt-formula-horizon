{%- from "horizon/map.jinja" import server with context %}
{%- if server.plugin is defined %}

{%- if server.get('plugin', {}).horizon_theme is defined %}

horizon_horizon_theme_package:
  pkg.installed:
  - name: {{ server.plugin.horizon_theme.source.name }}
  - watch_in:
    - service: horizon_services

{%- endif %}

{%- for plugin_name, plugin in server.get('plugin', {}).iteritems() %}

{%- if plugin_name != "horizon_theme" %}

horizon_{{ plugin_name }}_package:
  pkg.installed:
  - name: {{ plugin.source.name }}
  {%- if server.get('plugin', {}).horizon_theme is defined %}
  - require:
    - pkg: horizon_horizon_theme_package
  {%- endif %}
  - watch_in:
    - service: horizon_services

{%- endif %}

{%- endfor %}

{%- endif %}