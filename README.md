# Script for Implementing Cluster IP Failover for a Windows Failover Cluster on OCI

Microsoft Windows allows you to configure a [failover cluster](https://docs.microsoft.com/en-us/windows-server/failover-clustering/failover-clustering-overview).
As part of this configuration a single cluster IP address can be configured.  This IP address is hosted on the master node of the cluster and if the master node fails, it is automatically failed over to the new master node of the cluster.

As can be seen in the [documentation](https://docs.cloud.oracle.com/en-us/iaas/Content/Network/Tasks/managingIPaddresses.htm), on OCI, a vNIC can have one or more IP addresses assigned to it.  It will always have a primary IP address and can have multiple secondary IP addresses.  The IP address of each node in the cluster is assigned as the primary IP address of the vNIC assigned to that node.  The cluster IP address is assigned as a secondary IP address, initially to the vNIC of the master node in the cluster.  When the master node fails, whilst the Windows clusterware will fail the cluster IP address to the new master node automatically within the cluster, the secondary IP address also has to be reassigned to the vNIC of this new master node.  The script provided in the repo performs that functionality.

The script supports a 2 node failover cluster for Windows Server 2016 or Windows Server 2019 with an optional DR node in a different data center.  It was designed to provide failover for nodes running SQL Server and optionally you can configure a SQL Server cluster name and IP in which case the script will failover the IP for this cluster as well as for the default Windows failover cluster.

## Prerequisites


* A knowledge of Windows Server setup and administration is required.
* A 2 node Windows Failover Cluster must be setup and configured on OCI before using the script, and the node and cluster IP addresses defined in OCI.
* You should create a directory in an identical location of your choice on both nodes and place all the files from the repo in that directory.
* The script is written in [Python](https://www.python.org/downloads/) and uses the [OCI Python SDK](https://github.com/oracle/oci-python-sdk).
    * Both must be installed on both nodes of the cluster prior to installing and configuring the script.

## Configuration

The `oci_config` file is preformatted.  It has placed holders for the values required to configure the OCI Python SDK, these are documented [here](https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm).  Update it as appropriate. Please note add the real path for "key_file".  The script will use this file in preference to any config file you have already configured for the OCI Python SDK.

The `settings.json` configures the script for your specific environment.  It is preformated with placeholders.  Update it as appropriate:

```javascript
{
    "node1_name": "<Cluster Node Name 1>",  // Required Cluster Node Name 1
    "node2_name": "<Cluster Node Name 2>",  // Required Cluster Node Name 2
    "sql_cluster_name": "<sql cluster name>", // If SQL Server is in a cluster as well, specify the cluster name.  If not specified private_ip_id_sql_cluster will be ignored and is not required.
    "private_ip_id_default_cluster": "<ocid of windows cluster private IP>", // Required
    "private_ip_id_sql_cluster":"<ocid of SQL Server cluster private IP>", // Ignored if SQL Server cluster not present see above
    "skip_dr_node_name":"",  // If the cluster contains a DR node in a different DataCenter, specify its name here and it will be ignored by the script (which is for HA not DR)
    "vnic_1": "<ocid of Node 1 VNIC>", // Required
    "vnic_2": "<ocid of Node 2 VNIC>" // Required
}
```

To automatically start the script at boot time, import in Task Scheduler the XML file `oci-mscluster-scheduler.xml`. Remember to change the path to the script at <Command></Command>.

## Help
* The [Issues](https://github.com/oracle/cloud.asset.oci-msfailovercluster/issues) page of this GitHub repository.