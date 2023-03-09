from requests import exceptions
from cloud_resources.settings import ONEFS_URL, NFS_ROOT, VSPHERE, CLOUD_PATH
from .session import OneFSMixin
from urllib3.exceptions import InsecureRequestWarning
from pyVim import connect
from pyVmomi import vim, vmodl
from pyVim.task import WaitForTask
import yaml
import requests
import json
import urllib3

nfs_conn = OneFSMixin.get_session()
urllib3.disable_warnings(InsecureRequestWarning)


def get_nfs():
    url = ONEFS_URL + "platform/2/protocols/nfs/aliases?check=true"
    try:
        response = requests.get(url=url, auth=nfs_conn, verify=False)
        nfs_list = []
        nfs_id = []
        aliases = response.json().get("aliases")
        for aliase in aliases:
            usage = get_quotas(path=aliase.get("path").replace('/', '%2F'))
            nfs = {
                "id": aliase.get("id").replace('/', ''),
                "name": aliase.get("name"),
                "path": aliase.get("path"),
                "status": aliase.get("health"),
                "quota": usage.get("hard"),
                "used": usage.get("used"),
            }
            nfs_list.append(nfs)
            nfs_id.append(aliase.get("id").replace('/', ''))
    except exceptions.Timeout as e:
        print(e)
    except exceptions.HTTPError as e:
        print(e)
    else:
        return nfs_id, nfs_list


def get_quotas(path):
    url = ONEFS_URL + "platform/1/quota/quotas?path=" + path
    try:
        response = requests.get(url=url, auth=nfs_conn, verify=False)
        if not response.json().get("quotas"):
            usage = {
                "hard": 0,
                "used": 0
            }
            return usage
        quota = response.json().get("quotas")[0]
        usage = {
            "hard": quota.get("thresholds").get("hard"),
            "used": quota.get("usage").get("logical")
        }
        return usage
    except exceptions.Timeout as e:
        print(e)
    except exceptions.HTTPError as e:
        print(e)


def search_for_obj(content, vim_type, name, folder=None, recurse=True):
    """
    Search the managed object for the name and type specified
    Sample Usage:
    get_obj(content, [vim.Datastore], "Datastore Name")
    """
    if folder is None:
        folder = content.rootFolder

    obj = None
    container = content.viewManager.CreateContainerView(folder, vim_type, recurse)

    for managed_object_ref in container.view:
        if managed_object_ref.name == name:
            obj = managed_object_ref
            break
    container.Destroy()
    return obj


def get_all_obj(content, vim_type, folder=None, recurse=True):
    """
    Search the managed object for the name and type specified
    Sample Usage:
    get_obj(content, [vim.Datastore], "Datastore Name")
    """
    if not folder:
        folder = content.rootFolder

    obj = {}
    container = content.viewManager.CreateContainerView(folder, vim_type, recurse)

    for managed_object_ref in container.view:
        obj[managed_object_ref] = managed_object_ref.name

    container.Destroy()
    return obj


def get_obj(content, vim_type, name, folder=None, recurse=True):
    """
    Retrieves the managed object for the name and type specified
    Throws an exception if of not found.
    Sample Usage:
    get_obj(content, [vim.Datastore], "Datastore Name")
    """
    obj = search_for_obj(content, vim_type, name, folder, recurse)
    if not obj:
        raise RuntimeError("Managed Object " + name + " not found.")
    return obj


def _split_project_id(project_dir_name):
    """
    project_dir_name: "Project (3eadf579dcb04c7d980ecb235ea439ac)"
    return: "3eadf579dcb04c7d980ecb235ea439ac"
    """
    try:
        return project_dir_name.split('(')[1].split(')')[0]
    except Exception as e:
        raise Exception("split project_dir: %s failed: %s" % (project_dir_name, e))


def _split_vm_name_uuid(vm_dir_name):
    """
    vm_dir_name: "asdfghjk (8429558a-4606-48b7-80c4-982e59b82c1d)"
    return: ("asdfghjk", "8429558a-4606-48b7-80c4-982e59b82c1d")
    """
    try:
        return vm_dir_name[:-39], vm_dir_name[-37:-1]
        # arr = vm_dir_name.split('(')
        # if len(arr) == 3
        #     return arr[0].strip() + '(' + arr[1].strip(), arr[2].strip().split(')')[0]
        # return arr[0].strip(), arr[1].split(')')[0]
    except Exception as e:
        raise Exception("split vm_dir: %s failed: %s" % (vm_dir_name, e))


def show_vm(host, vm, dcName, project_id=""):
    vm_info = None

    try:
        location = "underlay"
        vm_name = vm.name
        vm_uuid = vm.summary.config.instanceUuid
        if project_id:
            location = "overlay"
            vm_name, vm_uuid = _split_vm_name_uuid(vm.name)
        summary = vm.summary
        tags = []
        for t in vm.tag:
            tags.append(t.key)
        if dcName == "CKDC":
            tags.append("新仓科机房")
        if dcName == "MWDC":
            tags.append("马尾机房")
        if dcName == "dc":
            tags.append("老仓科机房")

        vm_info = {
            "project_id": project_id,
            "uuid": vm_uuid,
            "guest_uuid": summary.config.uuid if summary.config.uuid else "",
            "name": vm_name,
            "hostName": summary.guest.hostName if summary.guest.hostName else "",
            "host": summary.runtime.host.name if summary.runtime.host.name else "",
            "cluster": summary.runtime.host.parent.name if summary.runtime.host.parent.name else "",
            "powerState": summary.runtime.powerState if summary.runtime.powerState else "",
            "ipAddress": vm.guest.ipAddress if vm.guest.ipAddress else "",
            "os": vm.guest.guestFullName if vm.guest.guestFullName else "",
            "osGuestId": vm.guest.guestId if vm.guest.guestId else "",
            "vCPU": summary.config.numCpu if summary.config.numCpu else 0,
            "vMemoryMB": summary.config.memorySizeMB if summary.config.numCpu else 0,
            "MemoryUsage": '{:.2%}'.format(
                float(summary.quickStats.guestMemoryUsage) / float(summary.config.memorySizeMB)),
            "cpuUsage": 0 if summary.quickStats.overallCpuUsage == 0 else '{:.2%}'.format(
                float(summary.quickStats.overallCpuUsage) / float(summary.runtime.maxCpuUsage)),
            "tags": tags,
            "remark": summary.config.annotation if summary.config.annotation else "",
            "managedBy": summary.config.managedBy.extensionKey if summary.config.managedBy else "",
            "location": location,
            "vSphereHost": host
        }
        return vm_info
    except Exception as e:
        print(e)
        # raise e

    return vm_info


def get_servers(host, user, pwd, port):
    try:
        vm_ins = connect.SmartConnect(host=host, user=user, pwd=pwd, port=port, disableSslCertValidation=True)
        content = vm_ins.RetrieveContent()
        container = content.rootFolder
        vm_type = [vim.VirtualMachine]
        recursive = True
        containerView = content.viewManager.CreateContainerView(container, vm_type, recursive)
        dc = content.viewManager.CreateContainerView(container, [vim.Datacenter], recursive).view[0]
        osfolder = get_obj(content, [vim.Folder], "OpenStack", dc.vmFolder)
        osvm = []
        dcName = dc.name
        for prject_folder in osfolder.childEntity:
            vm_list = []
            project_id = _split_project_id(prject_folder.name)
            os_vms_folder = get_obj(content, [vim.Folder], "Instances", prject_folder)
            os_volume_folder = get_obj(content, [vim.Folder], "Volumes", prject_folder)
            osvm.extend(os_vms_folder.childEntity)
            osvm.extend(os_volume_folder.childEntity)
            for vm in os_vms_folder.childEntity:
                vm_list.append(show_vm(host, vm, dcName, project_id))
                print(vm.summary.config.instanceUuid)
            yield vm_list
        vm_list = []
        for vm in containerView.view:
            if vm in osvm:
                continue
            print(vm.summary.config.instanceUuid)
            vm_list.append(show_vm(host=host, vm=vm, dcName=dcName))
        yield vm_list
    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)


def get_os_server(os_conn, server_id):
    return os_conn.get_server_by_id(server_id)


def show_volume(volume, os_conn):
    os_server = ''
    if volume.attachments:
        os_server = get_os_server(os_conn=os_conn, server_id=volume.attachments[0].get('server_id'))
    Volume = {
        'uuid': volume.id,
        'status': volume.status,
        'size': volume.size,
        'create_time': volume.created_at,
        'name': volume.name if volume.name else 'volume-'+volume.id,
        'volume_type': volume.volume_type,
        'user_id': volume.user_id,
        'is_bootable': volume.is_bootable,
        'attachments': volume.attachments[0] if volume.attachments else '',
        'host': volume.host,
        'region': volume.location.region_name,
        'server_ip': os_server.access_ipv4 if os_server else '',
    }
    return Volume


def get_vsphere():
    vsphere_list = []
    for vsphere in json.loads(VSPHERE):
        vSphere = {
            'user': vsphere.split(' ')[0],
            'pwd': vsphere.split(' ')[1],
            'host': vsphere.split(' ')[2],
            'port': int(vsphere.split(' ')[3])
        }
        vsphere_list.append(vSphere)
    return vsphere_list


def get_volumes(os_conn):
    volumes = []
    for volume in os_conn.block_storage.volumes(all_projects=True):
        volumes.append(show_volume(volume=volume, os_conn=os_conn))
    return volumes


def get_clouds():
    path = CLOUD_PATH
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f).get('clouds')
