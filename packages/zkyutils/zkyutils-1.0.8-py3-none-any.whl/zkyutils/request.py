import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from zkyutils.logger import log


retry_times = 5  # 设置重试次数
retry_backoff_factor = 0.5  # 设置重试间隔时间
timeout = 10  # 设置超时时间

session = requests.Session()
retry = Retry(total=retry_times, backoff_factor=retry_backoff_factor, status_forcelist=[500, 502, 503, 504], method_whitelist=["HEAD", "GET", "POST", "OPTIONS"])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


@log.log_decorator('网络请求')
def z_request(method, url, headers, data, resp_json=True):
    resp = session.request(method, url, headers=headers, data=data)
    if not resp_json:
        return {'success': True, 'msg': '', 'data': resp.text}
    try:
        resp.json()
    except Exception as e:
        return {'success': False, 'msg': str(e), 'data': resp.text}
    return {'success': True, 'msg': '', 'data': resp.json()}

