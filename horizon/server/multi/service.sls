{%- from "horizon/map.jinja" import server with context %}
{%- if server.enabled %}

include:
- git
- python

horizon_packages:
  pkg.installed:
  - names: {{ server.pkgs_multi }}
  - require:
    - pkg: python_packages

{%- if server.panel is defined %}

{%- for panel_name, panel in server.panel.iteritems() %}

horizon_panel_{{ panel_name }}:
  file.managed:
  - name: _{{ panel.priority }}_{{ panel.dashboard }}_{{ panel_name }}_panel.py
  - source: salt://horizon/files/enabled/panel.py
  - template: jinja
  - mode: 644
  - user: root
  - group: root
  - defaults:
    - panel_name: {{ panel_name }}
    - panel: {{ panel|yaml }}
  - require:
    - pkg: horizon_packages

{%- endfor %}

{%- endif %}

{%- endif %}

