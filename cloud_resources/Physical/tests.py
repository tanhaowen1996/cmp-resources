from pyVim import connect
from pyVmomi import vim

host_ins = connect.SmartConnect(host="10.209.1.254", user="yhcmp@yhcmpvc7-dev.local", pwd="m#ss9ttm2E", port=443,
                                disableSslCertValidation=True)
content = host_ins.RetrieveContent()
container = content.rootFolder
host_view = content.viewManager.CreateContainerView(container, [vim.HostSystem], True)
hosts = list(host_view.view)
host_view.Destroy()


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
    # import pdb
    #
    # pdb.set_trace()
    host = {
        'uuid': summary.hardware.uuid,
        'name': host_view.name,
        'ipaddress': host_view.name,
        'managementServerIp': summary.managementServerIp,
        'vnic': vnic_list,
        'vendor': summary.hardware.vendor,
        'hostModel': summary.hardware.model,
        'memorySize': summary.hardware.memorySize,
        'cpuMode': summary.hardware.cpuModel,
        'cpuMhz': summary.hardware.cpuMhz,
        'numCpuCores': summary.hardware.numCpuCores,
        'numCpuThreads': summary.hardware.numCpuThreads,
        'numCpuPkgs': summary.hardware.numCpuPkgs,
        'numNics': summary.hardware.numNics,
        'numHBAs': summary.hardware.numHBAs,
        'powerState': summary.runtime.powerState,
        'connectionState': summary.runtime.connectionState,
        'bootTime': summary.runtime.bootTime,
        'productName': config.product.name,
        'productFullName': config.product.fullName,
        'productVersion': config.product.version,
        'productPatchLevel': config.product.patchLevel,
        'productBuild': config.product.build,
        'productLocaleVersion': config.product.localeVersion,
        'productLocaleBuild': config.product.localeBuild,
        'productOsType': config.product.osType,
        'productProductLineId': config.product.productLineId,
        'licenseProductName': config.product.licenseProductName,
        'licenseProductVersion': config.product.licenseProductVersion,
        'overallCpuUsage': summary.quickStats.overallCpuUsage,
        'overallMemoryUsage': summary.quickStats.overallMemoryUsage,
        'distributedCpuFairness': summary.quickStats.distributedCpuFairness,
        'distributedMemoryFairness': summary.quickStats.distributedMemoryFairness,
        'availablePMemCapacity': summary.quickStats.availablePMemCapacity,
        'tags': tags,
    }
    import pdb

    pdb.set_trace()
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


if __name__ == '__main__':
    print('Start...')
    vms = get_hosts(host="10.209.1.254", user="yhcmp@yhcmpvc7-dev.local", pwd="m#ss9ttm2E", port=443)
    # vms2 = get_servers(host="10.0.115.239", user="yhcmp@yhcmpvc6.local", pwd="T%Tx9Tte8v", port=443)
    print('Done!')

s = ['AcquireCimServicesTicket', 'Array', 'ConfigureCryptoKey', 'Destroy', 'Destroy_Task', 'Disconnect',
     'DisconnectHost_Task', 'EnableCrypto', 'EnterLockdownMode', 'EnterMaintenanceMode', 'EnterMaintenanceMode_Task',
     'EnterStandbyMode', 'ExitLockdownMode', 'ExitMaintenanceMode', 'ExitMaintenanceMode_Task', 'ExitStandbyMode',
     'PowerDownHostToStandBy_Task', 'PowerUpHostFromStandBy_Task', 'PrepareCrypto', 'QueryConnectionInfo',
     'QueryHostConnectionInfo', 'QueryMemoryOverhead', 'QueryMemoryOverheadEx', 'QueryOverhead', 'QueryOverheadEx',
     'QueryProductLockerLocation', 'QueryTpmAttestationReport', 'Reboot', 'RebootHost_Task', 'ReconfigureDAS',
     'ReconfigureHostForDAS_Task', 'Reconnect', 'ReconnectHost_Task', 'Reload', 'Rename', 'Rename_Task',
     'RetrieveFreeEpcMemory', 'RetrieveHardwareUptime', 'SetCustomValue', 'Shutdown', 'ShutdownHost_Task',
     'UpdateFlags', 'UpdateIpmi', 'UpdateProductLockerLocation', 'UpdateProductLockerLocation_Task',
     'UpdateSystemResources', 'UpdateSystemSwapConfiguration', '_GetMethodInfo', '_GetMethodList', '_GetMoId',
     '_GetPropertyInfo', '_GetPropertyList', '_GetServerGuid', '_GetStub', '_InvokeAccessor', '_InvokeMethod',
     '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
     '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__',
     '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
     '__weakref__', '_methodInfo', '_moId', '_propInfo', '_propList', '_serverGuid', '_stub', '_version', '_wsdlName',
     'alarmActionsEnabled', 'answerFileValidationResult', 'answerFileValidationState', 'availableField', 'capability',
     'complianceCheckResult', 'complianceCheckState', 'config', 'configIssue', 'configManager', 'configStatus',
     'customValue', 'datastore', 'datastoreBrowser', 'declaredAlarmState', 'disabledMethod', 'effectiveRole',
     'hardware', 'licensableResource', 'name', 'network', 'overallStatus', 'parent', 'permission',
     'precheckRemediationResult', 'recentTask', 'remediationResult', 'remediationState', 'runtime', 'setCustomValue',
     'summary', 'systemResources', 'tag', 'triggeredAlarmState', 'value', 'vm']

config = ['Array', '_GetPropertyInfo', '_GetPropertyList', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__',
          '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__',
          '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__',
          '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_propInfo', '_propList',
          '_version', '_wsdlName', 'activeDiagnosticPartition', 'adminDisabled', 'assignableHardwareBinding',
          'assignableHardwareConfig', 'authenticationManagerInfo', 'autoStart', 'cacheConfigurationInfo',
          'capabilities', 'certificate', 'consoleReservation', 'datastoreCapabilities', 'datastorePrincipal',
          'dateTimeInfo', 'deploymentInfo', 'descriptionTreeCheckSum', 'domainList', 'dynamicProperty', 'dynamicType',
          'featureCapability', 'featureVersion', 'fileSystemVolume', 'firewall', 'flags', 'graphicsConfig',
          'graphicsInfo', 'host', 'hostConfigCheckSum', 'hyperThread', 'ioFilterInfo', 'ipmi', 'localSwapDatastore',
          'lockdownMode', 'maskedFeatureCapability', 'multipathState', 'network', 'offloadCapabilities', 'option',
          'optionDef', 'pciPassthruInfo', 'powerSystemCapability', 'powerSystemInfo', 'product', 'scriptCheckSum',
          'service', 'sharedGpuCapabilities', 'sharedPassthruGpuTypes', 'sriovDevicePool', 'sslThumbprintData',
          'sslThumbprintInfo', 'storageDevice', 'systemFile', 'systemResources', 'systemSwapConfiguration',
          'vFlashConfigInfo', 'virtualMachineReservation', 'virtualNicManagerInfo', 'vmotion', 'vsanHostConfig',
          'wakeOnLanCapable']
