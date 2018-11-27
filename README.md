# OCI-MS-Cluster

## In the archive you will find:

1. oci-mscluster.py - Python source code.
2. oci-ms-cluster-installer.exe - Windows installer created using Inno Setup.
  * oci_config - OCI configuration file used for Python OCI module.
  * settings.json - variables used in the script for switching a VIP from one node to another.
  * oci-mscluster.exe - Python script converted to Windows binary using PyInstaller.
  * oci-mscluster-scheduler.xml - XML for Windows Task Scheduler. The script will be added at Windows startup.
  * README.txt - short description of the script.
  * error.log - this file will be created when the script is running and will append changes encountered in the cluster environment.

In oci_config add the real path for "key_file".

In settings.json if you don't specify anything for "sql_cluster_name" the "private_ip_id_sql_cluster" will be ignored. The "oci-mscluster.exe" script has the default cluster "Cluster Group" already built in.

In settings.json "skip_dr_node_name" will be used if you have a DR setup (2 nodes on one DataCenter and one DR node on a different DataCenter). By specifying a name for "skip_dr_node_name" the script will ignore the DR node because it's on a different DataCenter and the VIP (virtual IP) address can not be moved.

To automatically start the script at boot time, import in Task Scheduler the XML file called "oci-mscluster-scheduler.xml". Remember to change the path to the script at <Command></Command>.

## Windows installer
https://oradocs-corp.documents.us2.oraclecloud.com/documents/link/LD9C457CFE9F8495CFA3A2B6F6C3FF17C1177A968060/fileview/DAB718BFC86E7FD133EE694BF6C3FF17C1177A968060/_oci-mscluster-12-jul-2018.zip