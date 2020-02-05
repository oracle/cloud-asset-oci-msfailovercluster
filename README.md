# OCI-MS-Cluster

Copyright © 2019, Oracle and/or its affiliates. All rights reserved.

The Universal Permissive License (UPL), Version 1.0

Subject to the condition set forth below, permission is hereby granted to any person obtaining a copy of this software, associated documentation and/or data
(collectively the "Software"), free of charge and under any and all copyright rights in the Software, and any and all patent rights owned or freely licensable
by each licensor hereunder covering either (i) the unmodified Software as contributed to or provided by such licensor, or (ii) the Larger Works (as defined below),
to deal in both

(a) the Software, and

(b) any piece of software and/or hardware listed in the lrgrwrks.txt file if one is included with the Software (each a “Larger Work” to which the Software is contributed by such licensors),

without restriction, including without limitation the rights to copy, create derivative works of, display, perform, and distribute the Software and make, use, sell, 
offer for sale, import, export, have made, and have sold the Software and the Larger Work(s), and to sublicense the foregoing rights on either these or other terms.

This license is subject to the following condition:

The above copyright notice and either this complete permission notice or at a minimum a reference to the UPL must be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## In the repo you will find:

1. oci-mscluster.py - Python source code.
2. oci_config - OCI configuration file used for Python OCI module.
3. settings.json - variables used in the script for switching a VIP from one node to another.
4. oci-mscluster-scheduler.xml - XML for Windows Task Scheduler. The script will be added at Windows startup.
5. LICENSE.TXT - License notice for this sample code
6. THIRD_PARTY_LICENSE.txt - Licenses applicable to use of this code.


In oci_config add the real path for "key_file".

In settings.json if you don't specify anything for "sql_cluster_name" the "private_ip_id_sql_cluster" will be ignored. The "oci-mscluster.exe" script has the default cluster "Cluster Group" already built in.

In settings.json "skip_dr_node_name" will be used if you have a DR setup (2 nodes on one DataCenter and one DR node on a different DataCenter). By specifying a name for "skip_dr_node_name" the script will ignore the DR node because it's on a different DataCenter and the VIP (virtual IP) address can not be moved.

To automatically start the script at boot time, import in Task Scheduler the XML file called "oci-mscluster-scheduler.xml". Remember to change the path to the script at <Command></Command>.

Full documentation available separately
