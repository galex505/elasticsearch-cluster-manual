.. index:: Nodes

Cluster Node setup
==================

Prerequisites
~~~~~~~~~~~~~

The following prerequisites have to be given:

* Server must be suitable for the Nextron base image.

* All nodes must be able to reach each other by resolving the fully qualified host name.

* TCP port 9300 must be open between all nodes (Note: API port 9200 is only used locally).

Elasticsearch node installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install the server from the Nextron ISO base image as you normally would
when installing the Analysis Cockpit itself, but **DO NOT** run the Nextron Installer.

Instead, copy ``es-node-install.sh`` to the new node and run it:

.. code-block:: console

    nextron@es-node1:~$ chmod +x es-node-install.sh
    nextron@es-node1:~$ sudo ./es-node-install.sh

The script will automatically install Elasticsearch and configure the node to
join the cluster with the Analysis Cockpit host as its master.

Resulting Elasticsearch configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Elasticsearch configuration can be found in ``/etc/elasticsearch/elasticsearch.yml``.
It will look like the following:

.. code-block:: yaml
    :linenos:

    cluster.name: elasticsearch
    cluster.routing.allocation.exclude._name: elastic-test-01.nextron
    path.data: /var/lib/elasticsearch
    path.logs: /var/log/elasticsearch
    node.roles: [ data, ingest ]
    http.host: _local:ipv4_
    transport.host: _site:ipv4_
    discovery.seed_hosts: [ elastic-test-01.nextron ]
    discovery.zen.minimum_master_nodes: 1
    xpack.security.transport.ssl.enabled: true
    xpack.security.transport.ssl.verification_mode: certificate
    xpack.security.transport.ssl.client_authentication: required
    xpack.security.transport.ssl.keystore.path: elastic-certificates.p12
    xpack.security.transport.ssl.truststore.path: elastic-certificates.p12

Enabling the node
~~~~~~~~~~~~~~~~~

After the installation, start elasticsearch and watch it becoming healthy:

.. code-block:: console

    nextron@es-node1:~$ sudo systemctl restart elasticsearch.service
    nextron@es-node1:~$ watch curl http://127.0.0.1:9200/_cluster/health

The node should automatically join the cluster.
