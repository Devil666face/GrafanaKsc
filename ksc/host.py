import KlAkOAPI.ChunkAccessor
import time
import csv
from KlAkOAPI.AdmServer import KlAkAdmServer
from KlAkOAPI.HostGroup import KlAkHostGroup
from KlAkOAPI.Updates import KlAkUpdates
from db.models import Updates
from datetime import datetime

class KscHostInfo:
    def __init__(self, server):
        self.server = server

    def get_host_dict(self):
        # self.fields_to_select =  ["KLHST_WKS_DN","KLHST_WKS_STATUS","KLHST_WKS_FQDN"]
        self.fields_to_select =  ["KLHST_WKS_FQDN","KLHST_WKS_STATUS"]
        str_accessor = KlAkOAPI.HostGroup.KlAkHostGroup(self.server).FindHosts("", self.fields_to_select, [], {'KLGRP_FIND_FROM_CUR_VS_ONLY': False}, lMaxLifeTime = 60 * 60).OutPar('strAccessor')
        chunk_accessor = KlAkOAPI.ChunkAccessor.KlAkChunkAccessor(self.server)    
        count = chunk_accessor.GetItemsCount(str_accessor).RetVal()      
        result_list = list()
        for start in range(0, count, 100):
            chunk = chunk_accessor.GetItemsChunk(str_accessor, start, 100)
            host_list = chunk.OutPar('pChunk')['KLCSP_ITERATOR_ARRAY']
            for obj in host_list:
                result_list.append([self.get_field(obj, field) for field in self.fields_to_select])
        return self.sorted_dict(hosts=result_list)
        
    def sorted_dict(self, hosts):
        host_dict = dict()
        for host in hosts:
            if not host[0] in host_dict:
                host_dict[host[0]] = [host[1]]
            else:
                host_active_list = host_dict[host[0]]
                host_active_list.append(host[1])

        return host_dict

    def get_field(self, obj, field_name):
        # print(obj)
        try:
            return obj[field_name]
        except:
            return "-"

    def get_updates(self):

        def get_str_date(date):
            return date.strftime('%Y-%m-%d')
        
        update_obj = KlAkUpdates(self.server)
        update_list = update_obj.GetUpdatesInfo([]).RetVal()
        Updates.objects.all().delete()
        for update in update_list:
            update_obj = Updates(title=update['FileName'], date=get_str_date(update['Date']))
            update_obj.save()
            # print(update_obj)
