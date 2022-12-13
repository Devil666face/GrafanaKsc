import re
import urllib3
import socket
import os
from pathlib import Path
from KlAkOAPI.HostGroup import KlAkHostGroup
from KlAkOAPI.ServerHierarchy import KlAkServerHierarchy
from db.models import ChildServer
from requests.exceptions import ConnectionError
from KlAkOAPI.AdmServer import KlAkAdmServer


class KscServer:
    def __init__(self, **kwargs):
        urllib3.disable_warnings()
        server_url = f"https://{socket.getfqdn(kwargs.get('ip',''))}:{kwargs.get('server_port','13299')}"
        path_to_SSL_verify_cert = Path(os.getcwd(),'klserver.cer')
        try:
            self.server = KlAkAdmServer.Create(server_url, kwargs.get('username'), kwargs.get('password'), verify = False)
            # server = self.server
            # print(self.server)
        except ConnectionError as ex:
            print(ex)
    
    def get_server(self):
        try:
            return self.server
        except AttributeError as ex:
            # print('Try to connection failed')
            return False

    def get_child_servers(self):
        child_server_list_obj = list()
        server_ierarchy = KlAkServerHierarchy(self.server)
        child_server_list = server_ierarchy.GetChildServers(-1).RetVal()
        # ChildServer.objects.all().delete()
        for child_server in child_server_list:
            server_ip, server_label = self.get_server_name(addr=child_server["KLSRVH_SRV_ADDR"], name=child_server["KLSRVH_SRV_DN"])
            server_active = child_server["KLSRVH_SRV_STATUS"]
            server_version = child_server["KLSRVH_SRV_VERSION"]
            server_last_connect = child_server["KLSRVH_SRV_LAST_CONNECTED"]
            child_server_obj = ChildServer(ip=server_ip, 
                                            label=server_label, 
                                            version=server_version, 
                                            last_connect = server_last_connect,
                                            active=server_active)
            child_server_list_obj.append(child_server_obj)
            child_server_obj.save()

        self.active_host_count()
        return child_server_list_obj
            
    def get_server_name(self, addr, name):
    
        def get_server_label(name):
            if name.find(' (')!=-1:
                return name.split(' (')[0]
            return name
                        
        server_ip = re.sub("[^0-9.:]", "", addr).split(':')[1] if addr else re.sub("[^0-9.]", "", name)
        server_label = get_server_label(name)
        return server_ip, server_label
    
    def active_host_count(self):
        active_host_param = KlAkHostGroup(self.server).GetInstanceStatistics(['KLSRV_ST_TOTAL_HOSTS_COUNT']).RetVal()
        self.active_host = active_host_param['KLSRV_ST_TOTAL_HOSTS_COUNT']
        
    def get_active_host_count(self):
        return self.active_host
