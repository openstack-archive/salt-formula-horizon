
=======
Horizon 
=======

Horizon is the canonical implementation of OpenStack’s Dashboard, which provides a web based user interface to OpenStack services including Nova, Swift, Keystone, etc.

Sample pillars
==============

Packaged version of horizon
---------------------------

One horizon on server

Simplest horizon setup with managed cloud-archive repo on ubuntu 12.04

.. code-block:: yaml

    linux:
      system:
        name: horizon
        repo:
         - cloudarchive-havana:
            enabled: true
            source: 'deb http://ubuntu-cloud.archive.canonical.com/ubuntu precise-updates/havana main'
            pgpcheck: 0
    horizon:
      server:
        manage_repo: true
        enabled: true
        secret_key: MEGASECRET
        host:
          name: cloud.lab.cz
        cache:
          engine: 'memcached'
          host: '127.0.0.1'
          port: 11211
          prefix: 'CACHE_HORIZON'
        identity:
          engine: 'keystone'
          host: '127.0.0.1'
          port: 5000
          api_version: 2
        mail:
          host: '127.0.0.1'

Simple branded horizon

.. code-block:: yaml

    horizon:
      server:
        enabled: true
        branding: 'OpenStack Company Dashboard'
        default_dashboard: 'admin'
        help_url: 'http://doc.domain.com'

Horizon package setup with SSL

.. code-block:: yaml

    horizon:
      server:
        enabled: true
        secret_key: MEGASECRET
        version: juno
        ssl:
          enabled: true
          authority: CA_Authority
        host:
          name: cloud.lab.cz
        cache:
          engine: 'memcached'
          host: '127.0.0.1'
          port: 11211
          prefix: 'CACHE_HORIZON'
        identity:
          engine: 'keystone'
          host: '127.0.0.1'
          port: 5000
          api_version: 2
        mail:
          host: '127.0.0.1'

Multi-regional horizon setup

.. code-block:: yaml

    horizon:
      server:
        enabled: true
        version: juno
        secret_key: MEGASECRET
        cache:
          engine: 'memcached'
          host: '127.0.0.1'
          port: 11211
          prefix: 'CACHE_HORIZON'
        identity:
          engine: 'keystone'
          host: '127.0.0.1'
          port: 5000
          api_version: 2
        mail:
          host: '127.0.0.1'
        regions:
        - name: cluster1
          address: http://cluster1.example.com:5000/v2.0
        - name: cluster2
          address: http://cluster2.example.com:5000/v2.0

Horizon setup with sensu plugin

.. code-block:: yaml

    horizon:
      server:
        enabled: true
        version: juno
        sensu_api:
          host: localhost
          port: 4567
        plugins:
        - name: monitoring
          app: horizon_monitoring
          source:
            type: git
            address: git@repo1.robotice.cz:django/horizon-monitoring.git
            rev: develop
        - name: api-mask
          app: api_mask
          mask_url: 'custom-url.cz'
          mask_protocol: 'http'
          source:
            type: git
            address: git@repo1.robotice.cz:django/horizon-api-mask.git
            rev: develop

Sensu multi API

.. code-block:: yaml

    horizon:
      server:
        enabled: true
        version: juno
        sensu_api:
          dc1:
            host: localhost
            port: 4567
          dc2:
            host: anotherhost
            port: 4567

Horizon setup with billometer plugin

.. code-block:: yaml

    horizon:
      server:
        enabled: true
        version: juno
        billometer_api:
          host: localhost
          port: 9753
          api_version: 1
        plugins:
        - name: billing
          app: horizon_billing
          source:
            type: git
            address: git@repo1.robotice.cz:django/horizon-billing.git
            rev: develop

Horizon setup with contrail plugin

.. code-block:: yaml

    horizon:
      server:
        enabled: true
        version: icehouse
        plugins:
        - name: contrail
          app: contrail_openstack_dashboard
          override: true
          source:
            type: git
            address: git@repo1.robotice.cz:django/horizon-contrail.git
            rev: develop

Horizon setup with sentry log handler

.. code-block:: yaml

    horizon:
      server:
        enabled: true
        version: juno
        ...
        logging:
          engine: raven
          dsn: http://pub:private@sentry1.test.cz/2

Multisite with Git source
-------------------------

Simple Horizon setup from git repository

.. code-block:: yaml

    horizon:
      server:
        enabled: true
        app:
          default:
            secret_key: MEGASECRET
            source:
              engine: git
              address: https://github.com/openstack/horizon.git
              rev: stable/havana
            cache:
              engine: 'memcached'
              host: '127.0.0.1'
              port: 11211
              prefix: 'CACHE_DEFAULT'
            identity:
              engine: 'keystone'
              host: '127.0.0.1'
              port: 5000
              api_version: 2
            mail:
              host: '127.0.0.1'

Themed multisite setup

.. code-block:: yaml

    horizon:
      server:
        enabled: true
        app:
          openstack1c:
            secret_key: MEGASECRET1
            source:
              engine: git
              address: https://github.com/openstack/horizon.git
              rev: stable/havana
            plugin:
              contrail:
                app: contrail_openstack_dashboard
                override: true
                source:
                  type: git
                  address: git@repo1.robotice.cz:django/horizon-contrail.git
                  rev: develop
              theme:
                app: site1_theme
                source:
                  type: git
                  address: git@repo1.domain.com:django/horizon-site1-theme.git
            cache:
              engine: 'memcached'
              host: '127.0.0.1'
              port: 11211
              prefix: 'CACHE_SITE1'
            identity:
              engine: 'keystone'
              host: '127.0.0.1'
              port: 5000
              api_version: 2
            mail:
              host: '127.0.0.1'
          openstack2:
            secret_key: MEGASECRET2
            source:
              engine: git
              address: https://repo1.domain.com/openstack/horizon.git
              rev: stable/icehouse
            plugin:
              contrail:
                app: contrail_openstack_dashboard
                override: true
                source:
                  type: git
                  address: git@repo1.domain.com:django/horizon-contrail.git
                  rev: develop
              monitoring:
                app: horizon_monitoring
                source:
                  type: git
                  address: git@domain.com:django/horizon-monitoring.git
                  rev: develop
              theme:
                app: bootswatch_theme
                source:
                  type: git
                  address: git@repo1.robotice.cz:django/horizon-bootswatch-theme.git
                  rev: develop
            cache:
              engine: 'memcached'
              host: '127.0.0.1'
              port: 11211
              prefix: 'CACHE_SITE2'
            identity:
              engine: 'keystone'
              host: '127.0.0.1'
              port: 5000
              api_version: 3
            mail:
              host: '127.0.0.1'

API versions override

.. code-block:: yaml

    horizon:
      server:
        enabled: true
        app:
          openstack_api_overrride:
            secret_key: MEGASECRET1
            api_versions:
              identity: 3
              volume: 2
            source:
              engine: git
              address: https://github.com/openstack/horizon.git
              rev: stable/havana

Control dashboard behaviour

.. code-block:: yaml

    horizon:
      server:
        enabled: true
        app:
          openstack_dashboard_overrride:
            secret_key: MEGASECRET1
            dashboards:
              settings:
                enabled: true
              project:
                enabled: false
                order: 10
              admin:
                enabled: false
                order: 20
            source:
              engine: git
              address: https://github.com/openstack/horizon.git
              rev: stable/juno

Read more
=========

* https://github.com/openstack/horizon
* http://dijks.wordpress.com/2012/07/06/how-to-change-screen-resolution-of-novnc-client-in-openstack-essex-dashboard-nova-horizon/


Things to improve
=================

* ALLOWED_HOSTS - do not use * - introduce parameters
* CACHES - configure caching engine - is it not allowed by default?
* SESSION_ENGINE - change it from signed cookie to something else
* policy files - look into these files and think of further configuration/parametrisation

Development and testing
=======================

Development and test workflow with `Test Kitchen <http://kitchen.ci>`_ and
`kitchen-salt <https://github.com/simonmcc/kitchen-salt>`_ provisioner plugin.

Test Kitchen is a test harness tool to execute your configured code on one or more platforms in isolation.
There is a ``.kitchen.yml`` in main directory that defines *platforms* to be tested and *suites* to execute on them.

Kitchen CI can spin instances locally or remote, based on used *driver*.
For local development ``.kitchen.yml`` defines a `vagrant <https://github.com/test-kitchen/kitchen-vagrant>`_ or
`docker  <https://github.com/test-kitchen/kitchen-docker>`_ driver.

To use backend drivers or implement your CI follow the section `INTEGRATION.rst#Continuous Integration`__.

A listing of scenarios to be executed:

.. code-block:: shell

  $ kitchen list

  Instance                    Driver   Provisioner  Verifier  Transport  Last Action

  cluster-ubuntu-1404  Vagrant  SaltSolo     Inspec    Ssh        <Not Created>
  cluster-ubuntu-1604  Vagrant  SaltSolo     Inspec    Ssh        <Not Created>
  cluster-centos-71    Vagrant  SaltSolo     Inspec    Ssh        <Not Created>
  single-ubuntu-1404   Vagrant  SaltSolo     Inspec    Ssh        <Not Created>
  single-ubuntu-1604   Vagrant  SaltSolo     Inspec    Ssh        <Not Created>
  single-centos-71     Vagrant  SaltSolo     Inspec    Ssh        <Not Created>

The `Busser <https://github.com/test-kitchen/busser>`_ *Verifier* is used to setup and run tests
implementated in `<repo>/test/integration`. It installs the particular driver to tested instance
(`Serverspec <https://github.com/neillturner/kitchen-verifier-serverspec>`_,
`InSpec <https://github.com/chef/kitchen-inspec>`_, Shell, Bats, ...) prior the verification is executed.


Usage:

.. code-block:: shell

 # list instances and status
 kitchen list

 # manually execute integration tests
 kitchen [test || [create|converge|verify|exec|login|destroy|...]] [instance] -t tests/integration

 # use with provided Makefile (ie: within CI pipeline)
 make kitchen

