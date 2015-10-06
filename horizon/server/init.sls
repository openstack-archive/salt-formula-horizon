include:
{%- if pillar.horizon.server.app is defined %}
{# uglier way, for development #}
- horizon.server.multi.service_git
- horizon.server.multi.site
{%- else %}
{# production way #}
- horizon.server.single
{%- endif %}
