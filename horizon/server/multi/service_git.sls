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

{%- endif %}

