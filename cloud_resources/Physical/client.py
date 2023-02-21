from requests import exceptions
from cloud_resources.settings import ONEFS_URL, NFS_ROOT, VSPHERE
from urllib3.exceptions import InsecureRequestWarning
from pyVim import connect
from pyVmomi import vim
import urllib3

urllib3.disable_warnings(InsecureRequestWarning)


def show_host(host_view):
    summary = host_view.summary
    config = host_view.config
    vnic_list = []
    for vnic in config.network.vnic:
        vnic_list.append({
            "ip": vnic.spec.ip.ipAddress,
            "subMask": vnic.spec.ip.subnetMask,
            "mac": vnic.spec.mac,
            "mtu": vnic.spec.mtu,
            "gateway": vnic.spec.ipRouteSpec.ipRouteConfig.defaultGateway,
        })
    tags = []
    for tag in host_view.tag:
        tags.append(tag)

    if summary.managementServerIp == "10.210.1.254":
        tags.append("新仓科机房")
    if summary.managementServerIp == "10.208.1.254":
        tags.append("马尾机房")
    if summary.managementServerIp == "10.0.115.239":
        tags.append("老仓科机房")
    if summary.managementServerIp == "10.209.1.254":
        tags.append("测试环境")
    host = {
        'uuid': summary.hardware.uuid,
        'name': host_view.name if host_view.name else '',
        'ipaddress': host_view.name if host_view.name else '',
        'managementServerIp': summary.managementServerIp if summary.managementServerIp else '',
        'cluster': host_view.parent.name if host_view.parent.name else '',
        'vnic': vnic_list,
        'vendor': summary.hardware.vendor if summary.hardware.vendor else '',
        'hostModel': summary.hardware.model if summary.hardware.model else '',
        'memorySize': summary.hardware.memorySize if summary.hardware.memorySize else '',
        'cpuModel': summary.hardware.cpuModel if summary.hardware.cpuModel else '',
        'cpuMhz': summary.hardware.cpuMhz if summary.hardware.cpuMhz else '',
        'numCpuCores': summary.hardware.numCpuCores if summary.hardware.numCpuCores else '',
        'numCpuThreads': summary.hardware.numCpuThreads if summary.hardware.numCpuThreads else '',
        'numCpuPkgs': summary.hardware.numCpuPkgs if summary.hardware.numCpuPkgs else '',
        'numNics': summary.hardware.numNics if summary.hardware.numNics else '',
        'numHBAs': summary.hardware.numHBAs if summary.hardware.numHBAs else '',
        'powerState': summary.runtime.powerState if summary.runtime.powerState else '',
        'connectionState': summary.runtime.connectionState if summary.runtime.connectionState else '',
        'bootTime': summary.runtime.bootTime if summary.runtime.bootTime else '',
        'productName': config.product.name if config.product.name else '',
        'productFullName': config.product.fullName if config.product.fullName else '',
        'productVersion': config.product.version if config.product.version else '',
        'productPatchLevel': config.product.patchLevel if config.product.patchLevel else '',
        'productBuild': config.product.build if config.product.build else '',
        'productLocaleVersion': config.product.localeVersion if config.product.localeVersion else '',
        'productLocaleBuild': config.product.localeBuild if config.product.localeBuild else '',
        'productOsType': config.product.osType if config.product.osType else '',
        'productProductLineId': config.product.productLineId if config.product.productLineId else '',
        'licenseProductName': config.product.licenseProductName if config.product.licenseProductName else '',
        'licenseProductVersion': config.product.licenseProductVersion if config.product.licenseProductVersion else '',
        'overallCpuUsage': summary.quickStats.overallCpuUsage if summary.quickStats.overallCpuUsage else '',
        'overallMemoryUsage': summary.quickStats.overallMemoryUsage if summary.quickStats.overallMemoryUsage else '',
        'distributedCpuFairness': summary.quickStats.distributedCpuFairness if summary.quickStats.distributedCpuFairness else '',
        'distributedMemoryFairness': summary.quickStats.distributedMemoryFairness if summary.quickStats.distributedMemoryFairness else '',
        'tags': tags,
    }
    return host


def get_hosts(host, user, pwd, port):
    host_ins = connect.SmartConnect(host=host, user=user, pwd=pwd, port=port, disableSslCertValidation=True)
    content = host_ins.RetrieveContent()
    container = content.rootFolder
    hosts_view = content.viewManager.CreateContainerView(container, [vim.HostSystem], True)
    hosts = []
    for host_view in hosts_view.view:
        hosts.append(show_host(host_view))
    hosts_view.Destroy()
    return hosts


def get_vsphere():
    vsphere_list = []
    for vsphere in VSPHERE:
        vSphere = {
            'user': vsphere.split(' ')[0],
            'pwd': vsphere.split(' ')[1],
            'host': vsphere.split(' ')[2],
            'port': int(vsphere.split(' ')[3])
        }
        vsphere_list.append(vSphere)
    return vsphere_list
