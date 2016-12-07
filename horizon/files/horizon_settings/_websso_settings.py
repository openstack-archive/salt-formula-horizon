{%- from "horizon/map.jinja" import server with context %}

{%- if server.websso is defined %}
{%- if server.websso.enabled %}
{%- if server.websso.login_url is defined %}
LOGIN_URL = {{ server.websso.login_url }}
{%- endif %}
{%- if server.websso.logout_url is defined %}
LOGOUT_URL = {{ server.websso.logout_url }}
{%- endif %}
WEBSSO_ENABLED = True
WEBSSO_CHOICES = (
    ("credentials", _("Keystone Credentials")),
    {%- if 'oidc' in server.websso.websso_choices %}
    ("oidc", _("OpenID Connect")),
    {%- endif %}
    {%- if 'saml2' in server.websso.websso_choices %}
    ("saml2", _("Security Assertion Markup Language")),
    {%- endif %}
)
WEBSSO_INITIAL_CHOICE = "credentials"
{%- endif %}
{%- endif %}
