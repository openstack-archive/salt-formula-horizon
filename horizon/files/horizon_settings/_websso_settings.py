{%- from "horizon/map.jinja" import server with context %}

{%- if server.websso.login_url is defined %}
LOGIN_URL = {{ server.websso.login_url }}
{%- endif %}
{%- if server.websso.logout_url is defined %}
LOGOUT_URL = {{ server.websso.logout_url }}
{%- endif %}
WEBSSO_ENABLED = True
WEBSSO_CHOICES = (
 ("credentials", _("Keystone Credentials")),
 ("saml2", _("Security Assertion Markup Language"))
)
WEBSSO_INITIAL_CHOICE = "credentials"
