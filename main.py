from ksc.server import KscServer
from ksc.host import KscHostInfo
from ksc.statistic import ServerStatistic
from ksc.config import username, password, server_port
from ksc.sorter import Sorter
from db.models import ChildServer, MainServer
from ksc.status import Status
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

def time(func):
    def wrapper_func():
        now = datetime.now()
        print(f'Start job {now}')
        func()
        print(f'Job finished {datetime.now()-now}')
    return wrapper_func
    

def save_main_server_stat(all_host, active_host_count):
    # MainServer.objects.all().delete()
    MainServer(all_host=all_host, active_host=active_host_count).save()

def save_main_server_updates(host_info):
    host_updates = host_info.get_updates()

@time
def main():
    print('Connect to server')
    server = KscServer(ip='10.16.5.225', 
                            username=username, 
                            password=password, 
                            server_port=server_port)
    print('Get server')
    host_info = KscHostInfo(server=server.get_server())
    print('Get all host')
    host_dict = host_info.get_host_dict()
    
    # Status(host_dict = host_dict).get_suspect_host()
    print('Get child servers')
    chield_server_list = server.get_child_servers()
    print('Get active hosts')
    active_host_count = server.get_active_host_count()
    print('Get updates')
    save_main_server_updates(host_info=host_info)
    
    save_main_server_stat(all_host=len(host_dict), active_host_count=active_host_count )

    print('Get active hosts for child servers')
    for server in chield_server_list:
        active_host_count = ServerStatistic(ip=server.ip,
                                            username=username,
                                            password=password,
                                            server_port=server_port,
                                            active=server.active,
                                            child_server=server).get_active_host_count()
        ChildServer.objects.filter(pk=server.pk).update(active_host = active_host_count)


if __name__=='__main__':
    print('Entry point')
    main()
    # scheduler = BackgroundScheduler()
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'interval', minutes=2)
    scheduler.start()
    # while True: pass
