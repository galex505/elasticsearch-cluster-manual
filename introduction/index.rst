.. index:: Introduction

Introduction
============

Analysis Cockpit Architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ASGARD Analysis Cockpit uses an Elasticsearch database to
store all event data. Each day worth of incoming events uses
a single Elasticsearch index.

Normally, Elasticsearch is running locally on the Analysis
Cockpit Server. However, when required Elasticsearch can easily
be extended to become a cluster of almost arbitrary size.

When running in Cluster mode, the Analysis Cockpit runs the
underlying metadata database and acts as the cluster master,
while all data is stored on the additional nodes.

When to consider Clustering
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You should consider extending the Elasticsearch installation
to become a cluster if:

* there is significant performance degradation
    
    * for searches that cover multiple days and/or

    * for adding events to cases.

* performance cannot be sufficiently improved by adding more
  CPU cores or faster disks (RAM is supported up to 32GB)

* disk size of the analysis cockpit cannot be increased but
  retention period requires additional storage

Performance
~~~~~~~~~~~

Benchmarks suggest there is a communication overhead of 10% - 20%
for a cluster compared to a single node in cases where a single
node would be sufficient for the given load.

As logs of one day are stored in one index and indices are distributed
over cluster members the performance gain will also depend on the
number of days stored in the cluster.

In a cluster configuration the former Analysis Cockpit will act a master
and will hold no data. Therefore, the minimum reasonable cluster size is
three. In such a minimum configuration we expect a performance gain of
60% given we have at least 60 days of logs.
