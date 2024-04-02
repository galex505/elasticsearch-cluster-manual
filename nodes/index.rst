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

Instead, copy ``/usr/share/asgard-analysis-cockpit/scripts/es-node-install.sh``
to the new node and run it:

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
    http.host: "_local:ipv4_"
    transport.host: "_site:ipv4_"
    discovery.seed_hosts: [ elastic-test-01.nextron ]
    search.default_allow_partial_results: false
    xpack.security.http.ssl.enabled: false
    xpack.security.enrollment.enabled: false
    xpack.security.transport.ssl:
        enabled: true
        verification_mode: certificate
        client_authentication: required
        keystore.path: elastic-certificates.p12
        truststore.path: elastic-certificates.p12

Enabling the node
~~~~~~~~~~~~~~~~~

After the installation, restart elasticsearch:

.. code-block:: console

    nextron@es-node1:~$ sudo systemctl restart elasticsearch.service

The node should automatically join the cluster. To check if the node has
joined the cluster, run the following command (``number_of_nodes`` should
be 1+X, where X is the number of nodes you have added):

.. code-block:: console
    :emphasize-lines: 6

    nextron@cockpit4:~$ curl -s http://127.0.0.1:9200/_cluster/health | jq
    {
      "cluster_name": "elasticsearch",
      "status": "green",
      "timed_out": false,
      "number_of_nodes": 4,
      "number_of_data_nodes": 4,
      "active_primary_shards": 10,
      "active_shards": 20,
      "relocating_shards": 0,
      "initializing_shards": 0,
      "unassigned_shards": 8,
      "delayed_unassigned_shards": 0,
      "number_of_pending_tasks": 0,
      "number_of_in_flight_fetch": 0,
      "task_max_waiting_in_queue_millis": 0,
      "active_shards_percent_as_number": 71.42857142857143
    }
