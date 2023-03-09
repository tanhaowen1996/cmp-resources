from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.utils.translation import gettext_lazy as _
from Virtual import client as virtual_client
import uuid
import logging

LOG = logging.getLogger(__name__)


# Create your models here.


class SyncPass(Exception):
    pass


def get_nfs():
    return virtual_client.get_nfs()


class Nfs(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=64,
        verbose_name=_('nfs id')
    )
    name = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    path = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=8,
        null=True,
        blank=True
    )
    quota = models.BigIntegerField(
        null=True,
        blank=True
    )
    used = models.BigIntegerField(
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated time'))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created time'))

    class Meta:
        indexes = (BrinIndex(fields=['updated_at', 'created_at']),)


def get_vsphere():
    return virtual_client.get_vsphere()


def get_servers(host, user, pwd, port):
    return virtual_client.get_servers(host, user, pwd, port)


class VServer(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    uuid = models.CharField(
        max_length=64,
        verbose_name=_('vServer id'),
        null=True,
        blank=True
    )
    project_id = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    guest_uuid = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    hostName = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    host = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    cluster = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    powerState = models.CharField(
        max_length=16,
        null=True,
        blank=True
    )
    ipAddress = models.CharField(
        max_length=32,
        null=True,
        blank=True
    )
    os = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    osGuestId = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    vCPU = models.IntegerField(
        null=True,
        blank=True
    )
    vMemoryMB = models.IntegerField(
        null=True,
        blank=True
    )
    MemoryUsage = models.CharField(
        max_length=16,
        null=True,
        blank=True
    )
    cpuUsage = models.CharField(
        max_length=16,
        null=True,
        blank=True
    )
    tags = models.JSONField(
        max_length=720,
        null=True,
        blank=True
    )
    remark = models.CharField(
        max_length=720,
        null=True,
        blank=True
    )
    managedBy = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    location = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    vSphereHost = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated time'))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created time'))

    class Meta:
        indexes = (BrinIndex(fields=['updated_at', 'created_at']),)


def get_clouds():
    return virtual_client.get_clouds()


def get_volumes(os_conn):
    return virtual_client.get_volumes(os_conn)


class Volume(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    uuid = models.CharField(
        max_length=64,
        verbose_name=_('volume id'),
        null=True,
        blank=True
    )
    size = models.FloatField(
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=32,
        null=True,
        blank=True
    )
    create_time = models.DateTimeField(
        null=True,
        blank=True
    )
    host = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    user_id = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    region = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    server_ip = models.CharField(
        max_length=32,
        null=True,
        blank=True
    )
    volume_type = models.CharField(
        max_length=32,
        null=True,
        blank=True
    )
    attachments = models.JSONField(
        max_length=720,
        null=True,
        blank=True
    )
    is_bootable = models.BooleanField(
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated time'))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created time'))

    class Meta:
        indexes = (BrinIndex(fields=['updated_at', 'created_at']),)
