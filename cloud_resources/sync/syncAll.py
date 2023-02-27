from apscheduler.schedulers.background import BackgroundScheduler
from cloud_resources.settings import WEBHOOK_URL
import requests
import json


def sync_host():
    print("start sync host")
    url = "http://localhost:8880/v2/host/sync_all"
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
    url = "http://localhost:8880/v2/vserver/sync_all"
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


scheduler = BackgroundScheduler(timezone="Asia/Shanghai")

scheduler.add_job(sync_host, 'cron', month='*', day='*', hour=23, minute=30, second=00)
scheduler.add_job(sync_vserver, 'cron', month='*', day='*', hour=23, minute=59, second=00)

scheduler.start()
