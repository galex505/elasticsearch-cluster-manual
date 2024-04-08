.. index:: Maintenance

Elasticsearch Node Maintenance
==============================

Performing Updates
~~~~~~~~~~~~~~~~~~

When updates are applied to the Analysis Cockpit, you also need to
update all additional cluster nodes by running:

.. code-block:: console
    
    nextron@es-node1:~$ sudo apt update
    nextron@es-node1:~$ sudo apt upgrade

It is recommended that you update one node at a time, in particular
when a reboot is required. It is not necessary to remove the node
from the cluster for the update.

Checking Elasticsearch status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can check elasticsearch status and index distribution on any of the nodes:

.. code-block:: console

    nextron@cockpit4:~$ sudo su -
    [sudo] password for nextron:
    root@cockpit4:~# curl -u elastic:$(cat /etc/asgard-analysis-cockpit/elastic.password) http://127.0.0.1:9200/_cat/health
    root@cockpit4:~# curl -u elastic:$(cat /etc/asgard-analysis-cockpit/elastic.password) http://127.0.0.1:9200/_cat/nodes
    root@cockpit4:~# curl -u elastic:$(cat /etc/asgard-analysis-cockpit/elastic.password) http://127.0.0.1:9200/_cat/shards
    root@cockpit4:~# curl -u elastic:$(cat /etc/asgard-analysis-cockpit/elastic.password) http://127.0.0.1:9200/_cluster/health | jq

Removing Elasticsearch nodes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before temporarily or permanently removing a node, you should reconfigure the
cluster to move away any shards from that node.

You can tell Elasticsearch to remove all indexes from a node (change the placeholder
value of "node_to_remove" to the actual node name):

.. code-block:: console

    nextron@cockpit4:~$ sudo su -
    [sudo] password for nextron:
    root@cockpit4:~$ curl -X PUT "http://127.0.0.1:9200/_cluster/settings" \
      -u elastic:$(cat /etc/asgard-analysis-cockpit/elastic.password) \
      -H "Content-Type: application/json" \
      -d '{"transient": {"cluster.routing.allocation.exclude._name": "node_to_remove"} }'
      

Then wait until the node has no shards left:

.. code-block:: console

    nextron@cockpit4:~$ curl -u elastic:$(cat /etc/asgard-analysis-cockpit/elastic.password) http://127.0.0.1:9200/_cat/shards

Once no shards are assigned to the node, it is safe to shut it down. When you have
replicas of each index (number_of_replicas >= 1), the cluster should automatically
cope with the removal of any single node. Refer to Elasticsearch documentation!

For obvious reasons, you must not remove the Analysis Cockpit node itself from the
cluster but it is ok to shut it down or restart it for maintenance.
