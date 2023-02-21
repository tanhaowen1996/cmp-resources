# from pyVim import connect
# from pyVmomi import vim
# from pyVim.task import WaitForTask
#
#
# vm_ins = connect.SmartConnect(host="10.209.1.254", user="yhcmp@yhcmpvc7-dev.local", pwd="m#ss9ttm2E", port=443, disableSslCertValidation=True)
# content = vm_ins.RetrieveContent()
# # 获取根路径容器
# container = content.rootFolder
# # 指定vim类型
# vm_type=[vim.VirtualMachine]
# recursive = True
# # 回去容器视图，这里面装的就是所有的VirtualMachine虚机
# containerView = content.viewManager.CreateContainerView(container, vm_type, recursive)
# obj = None
# for man_obj in content.viewManager.CreateContainerView(container, [vim.Datacenter], recursive).view:
#     if man_obj.name == 'dc':
#         obj = man_obj
#         break
# dc = obj
#
#
# osfolder = content.viewManager.CreateContainerView(dc.vmFolder, [vim.Folder], recursive)
#
# # for project_folder in osfolder.childEntity:
#
# for i in containerView.view:
#     import pdb
#     pdb.set_trace()
#     print(i.name, i.runtime.powerState)
#
# import pdb
# pdb.set_trace()




from pyVim import connect
from pyVmomi import vim


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
      arr = vm_dir_name.split('(')
      return arr[0].strip(), arr[1].split(')')[0]
    except Exception as e:
      raise Exception("split vm_dir: %s failed: %s" % (vm_dir_name, e))


def show_vm(vm, dcName, project_id=None):
    vm_info = None

    try:
        location = "underlay"
        vm_name = vm.name
        vm_uuid = vm.summary.config.instanceUuid
        print(vm.name)
        if project_id:
            location = "overlay"
            vm_name, vm_uuid = _split_vm_name_uuid(vm.name)
        summary = vm.summary
        tags = []
        for t in vm.tag:
            tags.append(t.name)
        if dcName == "CKDC":
            tags.append("新仓科机房")
        if dcName == "MWDC":
            tags.append("马尾机房")
        if dcName == "dc":
            tags.append("老仓科机房")

        vm_info = {
            "project_id": project_id,
            "id": vm_uuid,
            "guest_uuid": summary.config.uuid,
            "name": vm_name,
            "hostName": summary.guest.hostName,
            "host": summary.runtime.host.name,
            "cluster": summary.runtime.host.parent.name,
            "powerState": summary.runtime.powerState,
            "ipAddress": vm.guest.ipAddress if vm.guest.ipAddress else '',
            "os": vm.guest.guestFullName,
            "osGuestId": vm.guest.guestId,
            "vCPU": summary.config.numCpu,
            "vMemoryMB": summary.config.memorySizeMB,
            "MemoryUsage": '{:.2%}'.format(
                float(summary.quickStats.guestMemoryUsage) / float(summary.config.memorySizeMB)),
            "cpuUsage": 0 if summary.quickStats.overallCpuUsage == 0 else '{:.2%}'.format(
                float(summary.quickStats.overallCpuUsage) / float(summary.runtime.maxCpuUsage)),
            "tags": tags,
            "remark": summary.config.annotation if summary.config.annotation else "",
            "managedBy": summary.config.managedBy.extensionKey if summary.config.managedBy else "",
            "location": location,
        }
        return vm_info
    except Exception as e:
        print(e)
        # raise e

    return vm_info


def get_servers(host, user, pwd, port):
    vm_ins = connect.SmartConnect(host=host, user=user, pwd=pwd, port=port, disableSslCertValidation=True)
    content = vm_ins.RetrieveContent()
    container = content.rootFolder
    vm_type = [vim.VirtualMachine]
    recursive = True
    containerView = content.viewManager.CreateContainerView(container, vm_type, recursive)
    dc = content.viewManager.CreateContainerView(container, [vim.Datacenter], recursive).view[0]
    osfolder = get_obj(content, [vim.Folder], "OpenStack", dc.vmFolder)
    osvm = []
    vm_list = []
    dcName = dc.name
    for prject_folder in osfolder.childEntity:
        project_id = _split_project_id(prject_folder.name)
        os_vms_folder = get_obj(content, [vim.Folder], "Instances", prject_folder)
        os_volume_folder = get_obj(content, [vim.Folder], "Volumes", prject_folder)
        osvm.extend(os_vms_folder.childEntity)
        osvm.extend(os_volume_folder.childEntity)
        for vm in os_vms_folder.childEntity:
            vm_list.append(show_vm(vm, dcName, project_id))
    for vm in containerView.view:
        if vm in osvm:
            continue
        vm_list.append(show_vm(vm=vm, dcName=dcName))
    import pdb
    pdb.set_trace()
    return vm_list


if __name__ == '__main__':
    print('Start...')
    vms = get_servers(host="10.209.1.254", user="yhcmp@yhcmpvc7-dev.local", pwd="m#ss9ttm2E", port=443)
    vms2 = get_servers(host="10.0.115.239", user="yhcmp@yhcmpvc6.local", pwd="T%Tx9Tte8v", port=443)
    print('Done!')
