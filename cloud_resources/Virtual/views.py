from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import NfsSerializer, VServerSerializer, VolumeSerializer
from .models import Nfs, VServer, Volume, get_vsphere, get_servers, get_nfs, get_clouds, get_volumes
from .filters import NfsFilter, VServerFilter, VolumeFilter
from .session import create_connection
import logging

logger = logging.getLogger(__package__)


class NfsViewSet(viewsets.ModelViewSet):
    """
        list:
        Get NFS list

        create:
        Create NFS

        retrieve:
        Get NFS

        update:
        修改name

        destroy:
        drop NFS

        update_quota:
        修改文件系统容量
    """
    filterset_class = NfsFilter
    serializer_class = NfsSerializer
    queryset = Nfs.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        return NfsSerializer

    @action(detail=False, methods=['get'])
    def sync_nfs(self, request, *args, **kwargs):
        try:
            nfs_id, nfs_list = get_nfs()
            for db_nfs in Nfs.objects.all():
                if db_nfs.id not in nfs_id:
                    db_nfs.delete()
            for one_nfs in nfs_list:
                if not Nfs.objects.filter(id=one_nfs.get("id")):
                    serializer = self.get_serializer(data=one_nfs)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("同步完成", status=status.HTTP_200_OK)


class VServerViewSet(viewsets.ModelViewSet):
    """
            list:
            Get VServer list

            create:
            Create VServer

            retrieve:
            Get VServer

            update:
            修改name

            destroy:
            drop VServer
        """
    filterset_class = VServerFilter
    serializer_class = VServerSerializer
    queryset = VServer.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        return VServerSerializer

    @action(detail=False, methods=['get'])
    def sync_all(self, request, *args, **kwargs):
        try:
            vsphere_list = get_vsphere()
            for vsphere in vsphere_list:
                vserver_list = get_servers(host=vsphere.get('host'),
                                           user=vsphere.get('user'),
                                           pwd=vsphere.get('pwd'),
                                           port=vsphere.get('port'))
                vs_delete = VServer.objects.filter(vSphereHost=vsphere.get('host'))
                for vs in vs_delete:
                    vs.delete()
                for vm_list in vserver_list:
                    for vSphere in vm_list:
                        print(vSphere)
                        serializer = self.get_serializer(data=vSphere)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("同步完成", status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def sync(self, request, *args, **kwargs):
        try:
            vserver_list = get_servers(host=request.data.get('host'),
                                       user=request.data.get('user'),
                                       pwd=request.data.get('pwd'),
                                       port=request.data.get('port'))
            vs_delete = VServer.objects.filter(vSphereHost=request.data.get('host'))
            for vs in vs_delete:
                vs.delete()
            for vm_list in vserver_list:
                for vSphere in vm_list:
                    print(vSphere)
                    serializer = self.get_serializer(data=vSphere)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("同步完成", status=status.HTTP_200_OK)


class VolumeViewSet(viewsets.ModelViewSet):
    """
        list:
        Get Volume list

        create:
        Create Volume

        retrieve:
        Get Volume

        destroy:
        drop Volume
    """
    filterset_class = VServerFilter
    serializer_class = VolumeFilter
    queryset = VServer.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        return VolumeSerializer

    @action(detail=False, methods=['get'])
    def sync_all(self, request, *args, **kwargs):
        try:
            clouds = get_clouds()
            for cloud in clouds:
                os_conn = create_connection(auth_url=cloud.get('auth_url'),
                                            region=cloud.get('region'),
                                            project_name=cloud.get('project_name'),
                                            username=cloud.get('username'),
                                            password=cloud.get('password'),
                                            user_domain=cloud.get('user_domain'),
                                            project_domain=cloud.get('project_domain'))
                volumes = get_volumes(os_conn=os_conn)
                volumes_delete = Volume.objects.filter(region=cloud.get('region'))
                for volume in volumes_delete:
                    volume.delete()
                for volume in volumes:
                    print(volume)
                    serializer = self.get_serializer(data=volume)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("同步完成", status=status.HTTP_200_OK)
