{%- from "horizon/map.jinja" import server with context %}
{%- if server.enabled %}

include:
- horizon.server.multi.service

{%- endif %}
