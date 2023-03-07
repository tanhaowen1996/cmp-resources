from requests.auth import HTTPBasicAuth
from cloud_resources.settings import ONEFS_USER, ONEFS_PASSWORD
import openstack


class OneFSMixin:

    @staticmethod
    def get_session():
        nfs_session = HTTPBasicAuth(ONEFS_USER, ONEFS_PASSWORD)
        return nfs_session


def create_connection(auth_url, region, project_name, username, password, user_domain, project_domain):
    return openstack.connect(
        auth_url=auth_url,
        project_name=project_name,
        username=username,
        password=password,
        region_name=region,
        user_domain_name=user_domain,
        project_domain_name=project_domain, )
