from apscheduler.schedulers.background import BackgroundScheduler
from cloud_resources.settings import WEBHOOK_URL, SYNC_URL, SYNC_HOST_TIME, SYNC_VSERVER_TIME, SYNC_NFS_TIME, SYNC_VOLUME_TIME
import requests
import json


def sync_host():
    print("start sync host")
    url = "http://{sync_url}/v2/host/sync_all".format(sync_url=SYNC_URL)
    payload = {}
    headers = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)
        print("sync end-------")
    except Exception as e:
        webhook_url = WEBHOOK_URL
        content = "宿主机同步失败, detail: {}".format(e)
        data = {
            "msgtype": "markdown",
            "markdown": {"content": content}
        }
        requests.post(url=webhook_url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
                      verify=False)


def sync_vserver():
    print("start sync vserver")
    url = "http://{sync_url}/v2/vserver/sync_all".format(sync_url=SYNC_URL)
    payload = {}
    headers = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)
        print("sync end-------")
    except Exception as e:
        webhook_url = WEBHOOK_URL
        content = "云主机同步失败, detail: {}".format(e)
        data = {
            "msgtype": "markdown",
            "markdown": {"content": content}
        }
        requests.post(url=webhook_url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
                      verify=False)


def sync_nfs():
    print("start sync nfs")
    url = "http://{sync_url}/v2/nfs/sync_all".format(sync_url=SYNC_URL)
    payload = {}
    headers = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)
        print("sync end-------")
    except Exception as e:
        webhook_url = WEBHOOK_URL
        content = "文件存储同步失败, detail: {}".format(e)
        data = {
            "msgtype": "markdown",
            "markdown": {"content": content}
        }
        requests.post(url=webhook_url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
                      verify=False)


def sync_volume():
    print("start sync nfs")
    url = "http://{sync_url}/v2/volume/sync_all".format(sync_url=SYNC_URL)
    payload = {}
    headers = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)
        print("sync end-------")
    except Exception as e:
        webhook_url = WEBHOOK_URL
        content = "云硬盘同步失败, detail: {}".format(e)
        data = {
            "msgtype": "markdown",
            "markdown": {"content": content}
        }
        requests.post(url=webhook_url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
                      verify=False)


scheduler = BackgroundScheduler(timezone="Asia/Shanghai")

scheduler.add_job(sync_host, 'cron', month='*', day='*', hour=int(SYNC_HOST_TIME.split(':')[0]), minute=int(SYNC_HOST_TIME.split(':')[1]), second=int(SYNC_HOST_TIME.split(':')[2]))
scheduler.add_job(sync_vserver, 'cron', month='*', day='*', hour=int(SYNC_VSERVER_TIME.split(':')[0]), minute=int(SYNC_VSERVER_TIME.split(':')[1]), second=int(SYNC_VSERVER_TIME.split(':')[2]))
scheduler.add_job(sync_nfs, 'cron', month='*', day='*', hour=int(SYNC_NFS_TIME.split(':')[0]), minute=int(SYNC_NFS_TIME.split(':')[1]), second=int(SYNC_NFS_TIME.split(':')[2]))
scheduler.add_job(sync_volume, 'cron', month='*', day='*', hour=int(SYNC_VOLUME_TIME.split(':')[0]), minute=int(SYNC_VOLUME_TIME.split(':')[1]), second=int(SYNC_VOLUME_TIME.split(':')[2]))

scheduler.start()
