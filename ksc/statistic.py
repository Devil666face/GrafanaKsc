from ksc.server import KscServer
import KlAkOAPI.ChunkAccessor
from KlAkOAPI.AdmServer import KlAkAdmServer
from KlAkOAPI.HostGroup import KlAkHostGroup
from ksc.host import KscHostInfo

# class ServerStatistic(KscServer, KscHostInfo):
class ServerStatistic(KscServer):
    def __init__(self, **kwargs):
        active_status = bool(kwargs.get('active',0))
        
        self.child_server = kwargs.get('child_server',0)
        self.active_host = 0
        # Get server statistic only if server.active = 0
        
        # print(f'Status {active_status}')
        # self.server = self.check_active_status(active_status, kwargs)
        # print(self.server)
        # 
        # if not self.server:
            # print(self.server)
            # pass
        # else:
            # self.count_active_hosts()
            
        if active_status:
            super().__init__(**kwargs)
            self.server = super().get_server()
            
            if self.server:
                print(self.child_server.label)
                self.active_host_count()
                 
            # else:
                # print(f'self.server {active_status} for {kwargs}')
        # else:
            # print(f'Active status {active_status} for {kwargs}')

            
    def check_active_status(self, status, kwargs):
        print(f'check_active_status {status}')
        if status:
            print(f'check_active_status return false {status}')
            return False
        super().__init__(**kwargs)
        return super().get_server()

    def count_active_hosts(self):
        if not self.server: 
            return False
        self.active_host_count()
        # if self.server:
            # print(self.child_server.label)

    # def active_host_count(self):
        # active_host_param = KlAkHostGroup(self.server).GetInstanceStatistics(['KLSRV_ST_TOTAL_HOSTS_COUNT']).RetVal()
        # self.active_host = active_host_param['KLSRV_ST_TOTAL_HOSTS_COUNT']
        # 
    # def get_active_host_count(self):
        # return self.active_host
        
    # def get_host_dict(self):
        # if self.server:
            # return super().get_host_dict()
        # return False
        
