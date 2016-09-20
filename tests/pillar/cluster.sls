horizon:
  server:
    enabled: true
    version: liberty
    secret_key: secret
    session_timeout: 43200
    wsgi:
      processes: 3
      threads: 10
    bind:
      address: 127.0.0.1
      port: 80
    cache:
      engine: memcached
      prefix: 'CACHE_HORIZON'
      members: 
      - host: 127.0.0.1
        port: 11211
      - host: 127.0.0.1
        port: 11211
      - host: 127.0.0.1
        port: 11211
    identity:
      engine: keystone
      host: 127.0.0.1
      port: 5000
      api_version: 2
haproxy:
  proxy:
    listens:
    - name: horizon
      type: horizon
      binds:
      - address: 127.0.0.1
        port: 80
      servers:
      - name: ctl01
        host: 127.0.0.1
        port: 80
        params: cookie ctl01 check inter 2000 fall 3
      - name: ctl02
        host: 127.0.0.1
        port: 80
        params: cookie ctl02 check inter 2000 fall 3
      - name: ctl03
        host: 127.0.0.1
        port: 80
        params: cookie ctl03 check inter 2000 fall 3