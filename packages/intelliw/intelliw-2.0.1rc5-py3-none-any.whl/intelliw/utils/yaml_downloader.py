import sys
import time
import requests

requests.packages.urllib3.disable_warnings()

internal_aliyun = "intelliw-console.oss-cn-beijing-internal.aliyuncs.com"
yy_oss = "intelliw-console.diwork.com"


def download(url, path):
    for i in range(1, 5):
        try:
            if i == 2 and internal_aliyun in url:
                url = url.replace(internal_aliyun, yy_oss)
            resp = requests.get(url, verify=False, timeout=10.0)
            resp.raise_for_status()
            with open(path, "wb") as fp:
                fp.write(resp.content)
            return
        except requests.exceptions.RequestException as e:
            if i == 4:
                raise e
            time.sleep(i * 2)
            print(f"request retry time: {i}, url: {url}, error: {e}", flush=True)


if __name__ == '__main__':
    file_url = sys.argv[1]
    save_path = sys.argv[2]
    download(file_url, save_path)
