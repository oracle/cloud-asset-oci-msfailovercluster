# Copyright © 2020, Oracle and/or its affiliates. All rights reserved.
#
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.

import oci
import subprocess
import json
from datetime import datetime
import os, sys, time


signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
network = oci.core.VirtualNetworkClient(config={}, signer=signer)


history_nodes = []
history_nodes_sql = []


def error_log(message):
    error_log = open(os.path.dirname(os.path.realpath(sys.argv[0])) + '\error.log', 'a+b')
    error_log.write(str(datetime.now().strftime('%Y-%B-%d %H:%M:%S')) + ' ---> ' + message + '\n')
    error_log.close()


def no_variable():
    status_list = []
    list = ['node1_name', 'node2_name', 'private_ip_id_default_cluster', 'vnic_1', 'vnic_2']
    for i in list:
        if not str(settings[i]):
            print '!!! EMPTY ' + i + ' !!!'
            error_log('!!! EMPTY ' + i + ' !!!')
            status_list.append('nok')
        else:
            status_list.append('ok')
    if 'nok' in status_list:
        time.sleep(2)
        sys.exit()
    else:
        pass


try:
    file = open(os.path.dirname(os.path.realpath(sys.argv[0])) + '\settings.json', 'rb')
    settings = json.load(file)
    file.close()
except IOError:
    print '\n!!! No settings.json file !!!'
    error_log('No settings.json file')
    time.sleep(2)
    sys.exit()


no_variable()

default_cluster_name = 'Cluster Group'
if not str(settings['sql_cluster_name']):
    sql_cluster_name = ""
else:
    sql_cluster_name = str(settings['sql_cluster_name'])
node1_name = str(settings['node1_name'])
node2_name = str(settings['node2_name'])
private_ip_id_default_cluster = str(settings['private_ip_id_default_cluster'])
private_ip_id_sql_cluster = str(settings['private_ip_id_sql_cluster'])

if sql_cluster_name and not private_ip_id_sql_cluster:
    print '!!! EMPTY private_ip_id_sql_cluster !!!'
    error_log('!!! EMPTY private_ip_id_sql_cluster !!!')
    time.sleep(2)
    sys.exit()

skip_dr_node_name = str(settings['skip_dr_node_name'])
vnic_1 = str(settings['vnic_1'])
vnic_2 = str(settings['vnic_2'])


def assign_to_different_vnic(private_ip_id, vnic_id):
    update_private_ip_details = oci.core.models.UpdatePrivateIpDetails(vnic_id=vnic_id)
    network.update_private_ip(private_ip_id, update_private_ip_details)


def first_contact():
    cluster_group = subprocess.Popen(['C:\Windows\\sysnative\WindowsPowerShell\\v1.0\\powershell.exe','Get-ClusterGroup'], shell=True, stdout=subprocess.PIPE)
    cluster_group_read = cluster_group.communicate()[0].decode('utf-8')
    for var1 in cluster_group_read.splitlines():
        if var1.startswith(default_cluster_name):
            var2 = str(var1.split()[int(len(default_cluster_name.split(" ")))])
            if var2 == node1_name or var2 == node2_name or var2 == skip_dr_node_name:
                history_nodes.append(var2)
                print 'New MASTER DEFAULT NODE detected --> ' + var2
                error_log('New MASTER DEFAULT NODE detected --> ' + var2)
                if var2 == node1_name:
                    assign_to_different_vnic(private_ip_id_default_cluster, vnic_1)
                elif var2 == node2_name:
                    assign_to_different_vnic(private_ip_id_default_cluster, vnic_2)
                elif var2 == skip_dr_node_name:
                    pass
            else:
                print 'Invalid NODE'
                error_log('Invalid NODE --> ' + var2)
                time.sleep(2)
                sys.exit()
    if not sql_cluster_name:
        pass
    else:
        for var1 in cluster_group_read.splitlines():
            if var1.startswith(sql_cluster_name):
                var2 = str(var1.split()[int(len(sql_cluster_name.split(" ")))])
                if var2 == node1_name or var2 == node2_name or var2 == skip_dr_node_name:
                    history_nodes_sql.append(var2)
                    print 'New MASTER SQL NODE detected --> ' + var2
                    error_log('New MASTER SQL NODE detected --> ' + var2)
                    if var2 == node1_name:
                        assign_to_different_vnic(private_ip_id_sql_cluster, vnic_1)
                    elif var2 == node2_name:
                        assign_to_different_vnic(private_ip_id_sql_cluster, vnic_2)
                    elif var2 == skip_dr_node_name:
                        pass
                else:
                    print 'Invalid NODE'
                    error_log('Invalid NODE --> ' + var2)
                    time.sleep(2)
                    sys.exit()


first_contact()


while True:
    # print(history_nodes)
    # print(history_nodes_sql)
    cluster_group = subprocess.Popen(['C:\Windows\\sysnative\WindowsPowerShell\\v1.0\\powershell.exe', 'Get-ClusterGroup'], shell=True,stdout=subprocess.PIPE)
    cluster_group_read = cluster_group.communicate()[0].decode('utf-8')
    for var1 in cluster_group_read.splitlines():
        if var1.startswith(default_cluster_name):
            var2 = str(var1.split()[int(len(default_cluster_name.split(" ")))])
            if var2 == history_nodes[-1]:
                print 'Nothing to change on OCI, ' + var2 + ' is the MASTER DEFAULT NODE'
            else:
                if var2 == node1_name or var2 == node2_name or var2 == skip_dr_node_name:
                    print 'New MASTER DEFAULT NODE detected --> ' + var2
                    error_log('New MASTER DEFAULT NODE detected --> ' + var2)

                    if var2 == node1_name:
                        assign_to_different_vnic(private_ip_id_default_cluster, vnic_1)
                    elif var2 == node2_name:
                        assign_to_different_vnic(private_ip_id_default_cluster, vnic_2)
                    elif var2 == skip_dr_node_name:
                        pass
                    history_nodes.append(var2)

                    if len(history_nodes) > 3:
                        history_nodes = history_nodes[-3:]
                else:
                    print 'Invalid NODE'
                    error_log('Invalid NODE --> ' + var2)
    if not sql_cluster_name:
        pass
    else:
        cluster_group = subprocess.Popen(['C:\Windows\\sysnative\WindowsPowerShell\\v1.0\\powershell.exe', 'Get-ClusterGroup'], shell=True,stdout=subprocess.PIPE)
        cluster_group_read = cluster_group.communicate()[0].decode('utf-8')
        for var1 in cluster_group_read.splitlines():
            if var1.startswith(sql_cluster_name):
                var2 = str(var1.split()[int(len(sql_cluster_name.split(" ")))])
                if var2 == history_nodes_sql[-1]:
                    print 'Nothing to change on OCI, ' + var2 + ' is the MASTER SQL NODE'
                else:
                    if var2 == node1_name or var2 == node2_name or var2 == skip_dr_node_name:
                        print 'New MASTER SQL NODE detected --> ' + var2
                        error_log('New MASTER SQL NODE detected --> ' + var2)

                        if var2 == node1_name:
                            assign_to_different_vnic(private_ip_id_sql_cluster, vnic_1)
                        elif var2 == node2_name:
                            assign_to_different_vnic(private_ip_id_sql_cluster, vnic_2)
                        elif var2 == skip_dr_node_name:
                            pass
                        history_nodes_sql.append(var2)

                        if len(history_nodes_sql) > 3:
                            history_nodes_sql = history_nodes_sql[-3:]
                    else:
                        print 'Invalid NODE'
                        error_log('Invalid NODE --> ' + var2)

    time.sleep(1)
