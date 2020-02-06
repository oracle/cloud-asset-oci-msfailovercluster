# Script for Implementing a Windows Failover Cluster on OCI

Microsoft Windows allows you to configure a Failover Cluster - https://docs.microsoft.com/en-us/windows-server/failover-clustering/failover-clustering-overview.
As part of this configuration a single cluster IP address can be configured.  This IP address is hosted on the master node of the cluster and if the master node fails, it is automatically failed over to the new master node of the cluster.

As can be seen in the documention - https://docs.cloud.oracle.com/en-us/iaas/Content/Network/Tasks/managingIPaddresses.htm, on OCI, vNICs can have one or more IP addresses assigned to it.  It will always have a primary IP address and can have multiple secondary IP addresses.  The IP address of each node in the cluster is assigned as the primary IP address of the vNIC assigned to that node.  The cluster IP address is assigned as a secondary IP address, initially to the vNIC of the master node in the cluster.  When the master node fails, whilst the Windows clusterware will fail the cluster IP address to the new master node automatically within the cluster, the secondary IP address also has to be reassigned to the vNIC of this new master node.

The script provided in the repo performs that functionality.

## Prerequisites

The script supports a 2 node failover cluster for Windows Server 2016 or Windows Server 2019 with an optional DR node in a different data center.  It was designed to provide failover for nodes running SQL Server and optionally you can configure a SQL Server cluster name and IP in which case the script will failover the IP for this cluster as well as the default Windows failover cluster.  A knowledge of Windows Server setup and administration is required.  This should be setup before using the script and the node and cluster IP addresses defined in OCI.  The script is written in Python (https://www.python.org/downloads/) and uses the OCI Python SDK (https://github.com/oracle/oci-python-sdk).  Both must be installed prior to installing and configuring the script.  You should create a directory in a location of your choice and place all the files from the repo in that directory.

## In the repo you will find:

1. oci-mscluster.py - Python source code using user token for API access.
2. oci-mscluster-instance-principals.py - Python source code using instance principals for API access.
3. oci_config - This is the OCI configuration file for the OCI Python SDK used by the Python OCI module.
4. settings.json - variables used in the script for switching a VIP from one node to another.
5. oci-mscluster-scheduler.xml - XML for Windows Task Scheduler. The script must be added at Windows startup.
6. LICENSE.TXT - License notice for this sample code
7. THIRD_PARTY_LICENSE.txt - Licenses applicable to use of this code.

## Configuration

The oci_config file is preformatted.  It has placed holders for the values required to configure the OCI Python SDK, these are documented https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm.  Update it as appropriate. Please note add the real path for "key_file".

The settings.json configures the script for your specific environment.  It is preformated with placeholders.  Update it as appropriate:

{
    "node1_name": "<Cluster Node Name 1>",  -- Required Cluster Node Name 1
    "node2_name": "<Cluster Node Name 2>",  -- Required Cluster Node Name 2
    "sql_cluster_name": "<sql cluster name>", -- If SQL Server is in a cluster as well, specify the cluster name.  If not specified private_ip_id_sql_cluster will be ignored and is not required.
    "private_ip_id_default_cluster": "<ocid of windows cluster private IP>", -- Required
    "private_ip_id_sql_cluster":"<ocid of SQL Server cluster private IP>", -- Ignored if SQL Server cluster not present see above
    "skip_dr_node_name":"",  -- If the cluster contains a DR node in a different DataCenter, specify its name here and it will be ignored by the script (which is for HA not DR)
    "vnic_1": "<ocid of Node 1 VNIC>", -- Required
    "vnic_2": "<ocid of Node 2 VNIC>" -- Required
}


To automatically start the script at boot time, import in Task Scheduler the XML file called "oci-mscluster-scheduler.xml". Remember to change the path to the script at <Command></Command>.