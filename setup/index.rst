.. index:: Analysis Cockpit Setup

Analysis Cockpit Setup
======================

This chapter walks you through the necessary
steps to set up the Analysis Cockpit for use
with a cluster of Elasticsearch nodes.

Prerequisites
~~~~~~~~~~~~~

The Elasticsearch Cluster setup requires:

- A fully functional installation of Analysis Cockpit version 4.x
- At least two additional nodes with a similar high-end spec
- High-performance low-latency networking between all nodes
- All the nodes have a FQDN and can resolve each other's FQDNs and the Analysis Cockpit's FQDN

Analysis Cockpit preparation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After installation, the Analysis Cockpit runs with a single
local Elasticsearch instance as usual. To prepare it for use with
a cluster, run ``es-cluster-setup.sh``:

.. code-block:: console

    nextron@cockpit4:~$ sudo /usr/share/asgard-analysis-cockpit/scripts/es-cluster-setup.sh

The script will configure Elasticsearch in the following way:

- The Analysis Cockpit node continues to be the master node but data is automatically moved away from it once possible.
- SSL certificates are used for authentication of nodes.
- Any number of data nodes can be added with exactly the same configuration and certificate (as long as they are reachable).

.. hint::
    The script will display two errors (``xpack.security.transport.ssl...``)
    which can be ignored. These are due to the fact that the script
    is setting up the configuration for the cluster node.

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
    node.roles: [ master, data, ingest ]
    http.host: "_local:ipv4_"
    transport.host: "_site:ipv4_"
    discovery.seed_hosts: [ elastic-test-01.nextron ]
    cluster.initial_master_nodes: [ elastic-test-01.nextron ]
    search.default_allow_partial_results: false
    xpack.security.enabled: true
    xpack.security.enrollment.enabled: false
    xpack.security.http.ssl.enabled: false
    xpack.security.transport.ssl:
      enabled: true
      verification_mode: certificate
      client_authentication: required
      keystore.path: /etc/elasticsearch/elastic-certificates.p12
      truststore.path: /etc/elasticsearch/elastic-certificates.p12

The configuration:

- Designates the Analysis Cockpit node as the (only) cluster master.
- Automatically moves existing data away from the Analysis Cockpit node, and distributes it across the other nodes.
- TLS security is enabled so that nodes authenticate by certificate.

Cluster Node configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to reconfiguring the Analysis Cockpit, ``es-cluster-setup.sh`` will
create a configuration file ``clusternode.conf`` which contains the required
configuration for additional nodes to join the cluster. The file can be found
on your Analysis Cockpit in the home directory of the nextron user (``/home/nextron``).

If you executed the script as root user, the file will be located in
``/etc/asgard-analysis-cockpit/clusternode.conf``.

Download this configuration file for further usage in our Nextron
Universal Installer (:ref:`nodes/index:cluster node setup`).

Restarting Elasticsearch
~~~~~~~~~~~~~~~~~~~~~~~~

Finally, restart elasticsearch so that it picks up the new configuration:

.. code-block:: console

    nextron@cockpit4:~$ sudo systemctl restart elasticsearch

Your Analysis Cockpit is now ready to be used in a cluster setup.