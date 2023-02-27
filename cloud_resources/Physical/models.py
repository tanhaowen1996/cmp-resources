from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from django.utils.translation import gettext_lazy as _
from Physical import client as physical_client


def get_vsphere():
    return physical_client.get_vsphere()


def get_hosts(host, user, pwd, port):
    return physical_client.get_hosts(host, user, pwd, port)


class Host(models.Model):
    uuid = models.CharField(
        primary_key=True,
        max_length=64,
        verbose_name=_('Host uuid')
    )
    name = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    ipaddress = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    region = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        default="福州"
    )
    idc = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )
    managementServerIp = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )
    cluster = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )
    vnic = models.JSONField(
        max_length=720,
        null=True,
        blank=True,
    )
    vendor = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    hostModel = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    memorySize = models.BigIntegerField(
        null=True,
        blank=True,
    )
    cpuModel = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    cpuMhz = models.BigIntegerField(
        null=True,
        blank=True,
    )
    numCpuCores = models.IntegerField(
        null=True,
        blank=True,
    )
    numCpuThreads = models.IntegerField(
        null=True,
        blank=True,
    )
    numCpuPkgs = models.IntegerField(
        null=True,
        blank=True,
    )
    numNics = models.IntegerField(
        null=True,
        blank=True,
    )
    numHBAs = models.BigIntegerField(
        null=True,
        blank=True,
    )
    powerState = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    connectionState = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )
    bootTime = models.DateTimeField(
        null=True,
        blank=True,
    )
    productName = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )
    productFullName = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    productVersion = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    productPatchLevel = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    productBuild = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    productLocaleVersion = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    productLocaleBuild = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    productOsType = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    productProductLineId = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    licenseProductName = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    licenseProductVersion = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    overallCpuUsage = models.BigIntegerField(
        null=True,
        blank=True,
    )
    overallMemoryUsage = models.BigIntegerField(
        null=True,
        blank=True,
    )
    distributedCpuFairness = models.BigIntegerField(
        null=True,
        blank=True,
    )
    distributedMemoryFairness = models.BigIntegerField(
        null=True,
        blank=True,
    )
    tags = models.JSONField(
        max_length=720,
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated time'))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created time'))

    class Meta:
        indexes = (BrinIndex(fields=['updated_at', 'created_at']),)
