
{%- if pillar.horizon is defined %}
include:
{%- if pillar.horizon.server is defined %}
- horizon.server
{%- endif %}
{%- endif %}
