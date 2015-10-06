{%- from "horizon/map.jinja" import server with context %}

{%- for plugin in server.get('plugins', []) %}

{{ plugin }}_package:
  pkg.installed:
  - name: openstack-dashboard-{{ plugin }}
  - require:
    - pkg: horizon_packages
  - watch_in:
    - service: horizon_services
    - cmd: horizon_collectstatic

{%- endfor %}
