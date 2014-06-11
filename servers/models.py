# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.forms.util import ErrorList
from stat import S_ISDIR
import StringIO
import paramiko

PROVIDERS = (
    ('O', 'OVH'),
    ('H', 'Hetzner'),
    ('D', 'DigitalOcean'),
    ('A', 'Amazon'),
)

class Servers(models.Model):
    accounts = models.ForeignKey('billing.Accounts')
    cont_max = models.IntegerField(default=0)
    disk_max = models.IntegerField(default=0)
    memory = models.FloatField()
    cost_month = models.FloatField()
    provider = models.CharField(max_length=1, null=False, choices=PROVIDERS)
    ipaddr = models.GenericIPAddressField()
    rsa_key = models.TextField()

    def get_sftp(self):
        key = StringIO.StringIO(self.rsa_key)
        rsa_key = paramiko.RSAKey.from_private_key(key)
        self.trans = paramiko.Transport((self.ipaddr, 22))
        self.trans.connect(username="root", pkey=rsa_key)
        self.sftp = paramiko.SFTPClient.from_transport(trans)
        return sftp

    def close_sftp(self):
        self.sftp.close()
        self.trans.close()

OS = (
    ('D1', 'Debian 6 LTS'),
    ('D2', 'Debian 7.5'),
    ('U1', 'Ubuntu 13.10'),
    ('U2', 'Ubuntu 14.04'),
    ('C1', 'Centos 6.4'),
    ('C2', 'Centos 6.5'),
)

class Images(models.Model):
    token = models.CharField(max_length=64, null=False, unique=True)
    os = models.CharField(max_length=2, default='D2', null=False, choices=OS)
    accounts = models.ForeignKey('billing.Accounts', null=True)

class Disks(models.Model):
    accounts = models.ForeignKey('billing.Accounts')
    servers = models.ForeignKey('Servers')
    max_backups = models.IntegerField(default=0)
    path = models.CharField(max_length=100)
    size = models.IntegerField() # medido en bytes
    freq_backup = models.IntegerField() # medido en horas

    def dirs(self):
        sftp = servers.get_sftp()
        data = self._dirs(self.path, self.path)
        servers.close_sftp()
        return { '/': {
            'content': data, 'id': '/'
        }}

    def _dirs(self, hd, base, sftp):
        data = {}
        for entry in sftp.listdir_attr(hd):
            subdir = os.path.join(hd, entry.filename)
            if S_ISDIR(subdir.st_mode):
                data[entry.filename] = { 
                    'id': subdir[len(base)-1:], 
                    'content': self._dirs(subdir, base) 
                }
        return data

class Containers(models.Model):
    servers = models.ForeignKey('Servers')
    images = models.ForeignKey('Images')
    disks = models.ForeignKey('Disks')
    token = models.CharField(max_length=64, null=False, unique=True)
    ipaddr = models.GenericIPAddressField()
    port = models.IntegerField(null=False)

    class Meta:
        unique_together = ('servers', 'port')

class Backups(models.Model):
    disks = models.ForeignKey('Disks')
    created_at = models.DateField()
    size = models.IntegerField()
    path = models.CharField(max_length=100)
