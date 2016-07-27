horizon:
  server:
    enabled: true
    version: liberty
    secret_key: secret
    session_timeout: 43200
    bind:
      address: 127.0.0.1
      port: 80
    plugin:
      horizon_theme:
        theme_name: ubuntu
        source:
          engine: pkg
          name: openstack-dashboard-ubuntu-theme
    wsgi:
      processes: 3
      threads: 10
    mail:
      engine: dummy
    cache:
      engine: memcached
      prefix: 'CACHE_HORIZON'
      members:
      - host: 127.0.0.1
        port: 11211
    identity:
      engine: keystone
      port: 5000
      host: 127.0.0.1
      encryption: encryption
      api_version: 2
    websso:
      login_url: "WEBROOT + 'auth/login/'"
      logout_url: "WEBROOT + 'auth/logout/'"
      websso_choices:
        - saml2
        - oidc
