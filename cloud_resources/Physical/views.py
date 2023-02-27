from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import HostSerializer
from .models import Host, get_vsphere, get_hosts
from .filters import HostFilter
import logging

logger = logging.getLogger(__package__)
from sync.syncAll import scheduler


class HostViewSet(viewsets.ModelViewSet):
    """
    list:
    Get Host list

    create:
    Create Host

    retrieve:
    Get Host

    update:
    修改name

    destroy:
    drop Host
    """
    filterset_class = HostFilter
    serializer_class = HostSerializer
    queryset = Host.objects.all().order_by('-created_at')

    @action(detail=False, methods=['get'])
    def sync_all(self, request, *args, **kwargs):
        try:
            vsphere_list = get_vsphere()
            for vsphere in vsphere_list:
                host_list = get_hosts(host=vsphere.get('host'),
                                      user=vsphere.get('user'),
                                      pwd=vsphere.get('pwd'),
                                      port=vsphere.get('port'))
                Host_delete = Host.objects.filter(managementServerIp=vsphere.get('host'))
                for host in Host_delete:
                    host.delete()
                for host in host_list:
                    serializer = self.get_serializer(data=host)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("同步完成", status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def sync(self, request, *args, **kwargs):
        try:
            host_list = get_hosts(host=request.data.get('host'),
                                  user=request.data.get('user'),
                                  pwd=request.data.get('pwd'),
                                  port=request.data.get('port'))

            Host_delete = Host.objects.filter(managementServerIp=request.data.get('host'))
            for host in Host_delete:
                host.delete()
            for host in host_list:
                serializer = self.get_serializer(data=host)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("同步完成", status=status.HTTP_200_OK)
