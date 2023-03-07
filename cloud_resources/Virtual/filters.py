from django_filters import (
    FilterSet,
    CharFilter)
from .models import Nfs, VServer, Volume


class NfsFilter(FilterSet):
    id = CharFilter(field_name='id', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        mode = Nfs
        filter = ('name', 'id')


class VServerFilter(FilterSet):
    id = CharFilter(field_name='id', lookup_expr='icontains')
    uuid = CharFilter(field_name='id', lookup_expr='icontains')
    project_id = CharFilter(field_name='project_id', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    hostName = CharFilter(field_name='hostName', lookup_expr='icontains')
    host = CharFilter(field_name='host', lookup_expr='icontains')
    cluster = CharFilter(field_name='cluster', lookup_expr='icontains')
    powerState = CharFilter(field_name='powerState', lookup_expr='icontains')
    ipAddress = CharFilter(field_name='ipAddress', lookup_expr='icontains')
    managedBy = CharFilter(field_name='managedBy', lookup_expr='icontains')
    location = CharFilter(field_name='location', lookup_expr='icontains')
    vSphereHost = CharFilter(field_name='vSphereHost', lookup_expr='icontains')

    class Meta:
        mode = VServer
        filter = ('name', 'id',
                  'uuid',
                  'project_id',
                  'hostName',
                  'host',
                  'cluster',
                  'powerState',
                  'ipAddress',
                  'managedBy',
                  'location')


class VolumeFilter(FilterSet):
    id = CharFilter(field_name='id', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    uuid = CharFilter(field_name='uuid', lookup_expr='icontains')
    status = CharFilter(field_name='status', lookup_expr='icontains')
    host = CharFilter(field_name='host', lookup_expr='icontains')
    user_id = CharFilter(field_name='user_id', lookup_expr='icontains')
    region = CharFilter(field_name='region', lookup_expr='icontains')
    server_ip = CharFilter(field_name='server_ip', lookup_expr='icontains')
    volume_type = CharFilter(field_name='volume_type', lookup_expr='icontains')

    class Meta:
        mode = Volume
        filter = ('name', 'id',
                  'uuid',
                  'status',
                  'host',
                  'user_id'
                  'region',
                  'server_ip',
                  'volume_type')
