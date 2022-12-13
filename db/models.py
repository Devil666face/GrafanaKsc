from django.db import models
from manage import init_django
from datetime import datetime

init_django()


class Model(models.Model):
    id = models.AutoField(primary_key=True)
    # created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

def get_rfc_datetime():
    # return datetime.today().strftime('%Y-%m-%dT%H:%M:%S')+'Z'
    return datetime.today().strftime('%Y-%m-%dT%H:%M:%S')+'+03:00'

class ChildServer(Model):
    # updated_at = models.DateTimeField(auto_now=True)
    updated_at = models.CharField(max_length=255, default='date')
    ip = models.CharField(max_length=255, blank=False, null=False, default='chield server ip') #db_index=True, 
    label = models.CharField(max_length=255, blank=False, null=False, default='chield server name') #db_index=True, 
    version = models.CharField(max_length=255, blank=False, null=False, default='chield server version')
    last_connect = models.CharField(max_length=255, blank=False, null=False, default='chield server version')
    active = models.BooleanField(default='False')
    active_host = models.IntegerField(default=0)
    
    def __str__(self):
        return self.ip

    def save(self, *args, **kwargs):
        self.updated_at = get_rfc_datetime()
        super(ChildServer, self).save(*args, **kwargs)

class Updates(Model):
    title = models.CharField(max_length=255, blank=False, null=False, default='base name')
    date = models.CharField(max_length=255, blank=False, null=False, default='base date')

    def __str__(self):
        return f'{self.title} {self.date}'

class SuspectHost(Model):
    host_name = models.CharField(max_length=255, blank=False, null=False, default='hostname')
    host_in_lan = models.BooleanField(default='False')
    agent_install = models.BooleanField(default='False')
    agent_active = models.BooleanField(default='False')
    instance_protect = models.BooleanField(default='False')

    def __str__(self):
        return f'{self.host_name} {self.host_in_lan} {self.agent_install} {self.agent_active} {self.instance_protect} {self.agent_install}'

class MainServer(Model):
    updated_at = models.CharField(max_length=255, default='date')
    # updated_at = models.DateTimeField(auto_now=True)
    all_host = models.IntegerField(default=0)
    active_host = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.all_host} {self.active_host}'

    
    def save(self, *args, **kwargs):
        self.updated_at = get_rfc_datetime()
        super(MainServer, self).save(*args, **kwargs)
