# Script for Implementing a Windows Failover Cluster on OCI

Microsoft Windows allows you to configure a Failover Cluster - https://docs.microsoft.com/en-us/windows-server/failover-clustering/failover-clustering-overview.
As part of this configuration a single cluster IP address can be configured.  This IP address is hosted on the master node of the cluster and if the master node fails, it is automatically failed over to the new master node of the cluster.

As can be seen in the documention - https://docs.cloud.oracle.com/en-us/iaas/Content/Network/Tasks/managingIPaddresses.htm, on OCI, vNICs can have one or more IP addresses assigned to it.  It will always have a primary IP address and can have multiple secondary IP addresses.  The IP address of each node in the cluster is assigned as the primary IP address of the vNIC assigned to that node.  The cluster IP address is assigned as a secondary IP address, initially to the vNIC of the master node in the cluster.  When the master node fails, whilst the Windows clusterware will fail the cluster IP address to the new master node automatically within the cluster, the secondary IP address also has to be reassigned to the vNIC of this new master node.

The script provided in the repo performs that functionality.

## Prerequisites

The script supports Windows Server 2016 and Windows Server 2019 failover clustering.  This should be setup before using the script and the node and cluster IP addresses defined in OCI.  The script is written in Python (https://www.python.org/downloads/) and uses the OCI Python SDK (https://github.com/oracle/oci-python-sdk).  Both must be installed prior to installing and configuring the script.

## In the repo you will find:

1. oci-mscluster.py - Python source code using user token for API access.
2. oci-mscluster-instance-principals.py - Python source code using instance principals for API access.
3. oci_config - This is the OCI configuration file used for Python OCI module.  This should be placed in the .oci directory created by the OCI Python SDK and renamed config or referenced on the command line.
4. settings.json - variables used in the script for switching a VIP from one node to another.
5. oci-mscluster-scheduler.xml - XML for Windows Task Scheduler. The script will be added at Windows startup.
6. LICENSE.TXT - License notice for this sample code
7. THIRD_PARTY_LICENSE.txt - Licenses applicable to use of this code.

## Configuration

In oci_config add the real path for "key_file".

In settings.json if you don't specify anything for "sql_cluster_name" the "private_ip_id_sql_cluster" will be ignored. The script has the default cluster "Cluster Group" already built in.

In settings.json "skip_dr_node_name" will be used if you have a DR setup (2 nodes on one DataCenter and one DR node on a different DataCenter). By specifying a name for "skip_dr_node_name" the script will ignore the DR node because it's on a different DataCenter and the VIP (virtual IP) address can not be moved.

To automatically start the script at boot time, import in Task Scheduler the XML file called "oci-mscluster-scheduler.xml". Remember to change the path to the script at <Command></Command>.

Full documentation available separately
