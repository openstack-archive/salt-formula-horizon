include:
{%- if pillar.horizon.server.app is defined %}
{# uglier way, for development #}
- horizon.server.multi.service
- horizon.server.multi.site
{%- else %}
{# production way #}
- horizon.server.service
{%- if pillar.horizon.server.plugin is defined %}
- horizon.server.plugin
{%- endif %}
{%- if pillar.horizon.server.ssl is defined %}
- horizon.server.ssl
{%- endif %}
{%- endif %}
