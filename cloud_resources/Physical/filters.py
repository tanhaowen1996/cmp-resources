from django_filters import (
    FilterSet,
    CharFilter)
from .models import Host


class HostFilter(FilterSet):
    uuid = CharFilter(field_name='uuid', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    ipaddress = CharFilter(field_name='ipaddress', lookup_expr='icontains')
    managementServerIp = CharFilter(field_name='managementServerIp', lookup_expr='icontains')
    cluster = CharFilter(field_name='cluster', lookup_expr='icontains')
    vendor = CharFilter(field_name='vendor', lookup_expr='icontains')
    hostModel = CharFilter(field_name='hostModel', lookup_expr='icontains')
    cpuModel = CharFilter(field_name='cpuMode', lookup_expr='icontains')
    powerState = CharFilter(field_name='powerState', lookup_expr='icontains')
    connectionState = CharFilter(field_name='connectionState', lookup_expr='icontains')
    productName = CharFilter(field_name='productName', lookup_expr='icontains')
    productFullName = CharFilter(field_name='productFullName', lookup_expr='icontains')
    productVersion = CharFilter(field_name='productVersion', lookup_expr='icontains')
    productPatchLevel = CharFilter(field_name='productPatchLevel', lookup_expr='icontains')
    productBuild = CharFilter(field_name='productBuild', lookup_expr='icontains')
    productLocaleVersion = CharFilter(field_name='productLocaleVersion', lookup_expr='icontains')
    productLocaleBuild = CharFilter(field_name='productLocaleBuild', lookup_expr='icontains')
    productOsType = CharFilter(field_name='productOsType', lookup_expr='icontains')
    productProductLineId = CharFilter(field_name='productProductLineId', lookup_expr='icontains')
    licenseProductName = CharFilter(field_name='licenseProductName', lookup_expr='icontains')
    licenseProductVersion = CharFilter(field_name='licenseProductVersion', lookup_expr='icontains')

    class Meta:
        mode = Host
        filter = '__all__'
