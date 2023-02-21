from pyVim import connect
from pyVmomi import vim
from pyVim.task import WaitForTask


class VCMixin:

    @staticmethod
    def get_session():
        vc_session = connect.SmartConnect(host="", user="", pwd="", port=443)
        return vc_session
