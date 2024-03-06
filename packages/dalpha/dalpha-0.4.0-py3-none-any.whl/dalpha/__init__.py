import requests, json, boto3, io, logging, sys, os, pkg_resources
import time
import sentry_sdk
from dalpha.signal_handler import get_shutdown_requested
from requests.adapters import HTTPAdapter, Retry
from dalpha.context import clear_context_evaluate, set_context, set_context_evaluate, Context
from dalpha.logging import logger
from dalpha.logging.events import Event

def __load_config(file_path):
    if not os.path.isfile(file_path):
        logger.warning(f"{file_path} 파일을 찾을 수 없습니다.")
        return
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            key, value = line.split("=")
            os.environ[key] = value

def get_env_var_or_raise(var_name):
    """
    환경변수를 가져오거나 없으면 에러를 발생시킴
    """
    value = os.environ.get(var_name)
    if value is None:
        raise ValueError(f"Environment variable {var_name} is not set")
    return value

def check_package_version(package_name):
    installed_version = pkg_resources.get_distribution(package_name).version
    try:
        url = f"https://pypi.org/pypi/{package_name}/json"
        response = requests.get(url)
        data = response.json()
        latest_version = data["info"]["version"]
        if latest_version != installed_version:
            logger.warning(" dalpha sdk 버전 -> " + installed_version + " / 최신 버전 -> " + latest_version)
        else:
            logger.info(" dalpha sdk 버전 -> " + installed_version + " (latest)")
    except Exception as e:
        logger.warning(f"dalpha sdk 버전 확인 중 오류가 발생했습니다:{e}")
cfg_path = os.path.join(sys.path[0],'.dalphacfg')
__load_config(cfg_path)
check_package_version("dalpha")

class DalphaRedis:
    def __init__(self, client: str, db_num: int):
        self.rd = self.setup(db_num)
        self.client = client

    def setup(self, db_num):
        try:
            import redis
            from redis.backoff import ExponentialBackoff
            from redis.retry import Retry
            from redis.exceptions import (
            BusyLoadingError,
            ConnectionError,
            TimeoutError
            )
            retry = Retry(ExponentialBackoff(), 3)

        except ImportError:
            raise ImportError("Please install redis-py package -> pip install redis")
        
        return redis.StrictRedis(
            host="k8s-redis-redis-8a93856597-98eab959ed2cbb3e.elb.ap-northeast-2.amazonaws.com",
            port=6379,
            decode_responses=True,
            password=os.environ.get("REDIS_PASSWORD"),
            retry = retry,
            retry_on_error = [BusyLoadingError, ConnectionError, TimeoutError],
            db = db_num
        )

    def get(self, key: str):
        key = f"{self.client}-{key}"
        json_dict = self.rd.get(key)
        if json_dict:

            return_lst = json.loads(json_dict)
            return return_lst
        else:
            return None

    def set(self, key: str, value, expire: int = None):
        key = f"{self.client}-{key}"
        try:
            json_dict = json.dumps(value, ensure_ascii=False).encode("utf-8")
            self.rd.set(key, json_dict, ex=expire)
            return True
        except Exception as e:
            logger.error(f"Error : {e}")
            return False

    def delete(self, key: str):
        key = f"{self.client}-{key}"
        try:
            self.rd.delete(key)
            return True
        except Exception as e:
            logger.error(f"Error : {e}")
            return False

class Agent:
    def __init__(self, api_id, use_sqs=bool(os.environ.get('USE_SQS', 'False') == 'True'), dev_server=bool(os.environ.get('DEV_SERVER', 'True') == 'True')):
        if not isinstance(api_id, int): raise TypeError('api_id is not a int')
        if not isinstance(use_sqs, bool): raise TypeError('use_sqs is not a bool')
        if not isinstance(dev_server, bool): raise TypeError('dev_server is not a bool')
        self.token = os.environ['TOKEN']
        self.sentry_dsn = os.environ['SENTRY_DSN']
        self.max_retry = 5
        if dev_server:
            self.base_url = os.environ.get('DEV_BASE_URL', 'https://api.exp.dalpha.so')
            self.sentry_env = "exp"
        else:
            self.base_url = os.environ.get('BASE_URL', 'https://api.dalpha.so')
            self.sentry_env = "production"
        self.queue_url = os.environ.get('QUEUE_URL',None)
        headers = {
        'token': self.token
        }
        response = requests.request("GET", os.path.join(self.base_url,f"inferences/{api_id}"), headers = headers)
        if response.status_code != 200:
            logger.warning(f'error from get sqs url / response status_code {response.status_code}: {response.text}')
        else:
            if self.queue_url is None:
                self.queue_url = response.json().get('sqs', None)
            self.service_code = response.json().get('serviceCode', None)

        if self.queue_url is None:
            logger.warning("sqs url is not set")

        self.evaluate_url = os.path.join(self.base_url, f"inferences/{api_id}/evaluate")
        self.api_id = api_id
        self.mock = {}
        self.s3 = boto3.client('s3')
        self.sqs = boto3.client('sqs', region_name='ap-northeast-2')
        self.evaluates = {}
        self.use_sqs = use_sqs
        set_context(Context(
            inference_id = api_id,
            service_code = self.service_code,
            env = "exp" if dev_server else "prod"
        ))

        sentry_sdk.init(
            dsn=self.sentry_dsn,

            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=1.0,
            environment = self.sentry_env
        )
        sentry_sdk.set_tag("api_id", api_id)
        logger.info(
            message = "Dalpha agent initialized",
            event = Event.AGENT_INIT,
            data = {
                'inference_id': api_id,
                "use_sqs": use_sqs,
                "dev_server": dev_server,
                "base_url": self.base_url,
                "queue_url": self.queue_url,
                "sentry_dsn": self.sentry_dsn,
            }
        )

    def set_mock(self, mock):
        self.mock = mock

    def batch(self, iterable, n):
        # Yield successive n-sized chunks from iterable.
        for i in range(0, len(iterable), n):
            yield iterable[i:i + n]
    
    '''
        message_id를 10개씩 끊어서 sqs에 batch delete 요청으로 메세지 삭제
    '''
    def delete_messages(self, message_ids):
        entries = list(map(lambda message_id: {
            'Id': str(message_id),
            'ReceiptHandle': self.evaluates[message_id]
        }, message_ids))
        for group in self.batch(entries, 10):
            try:
                self.sqs.delete_message_batch(
                    QueueUrl = self.queue_url,
                    Entries = group
                )
            except Exception as e:
                logger.error(f"Error while deleting messages\n{e}")
    
    '''
        evaluate이 유효한지 서버에 요청해서 유효하지 않은 메세지는 sqs에서 삭제
        유효한 메세지만 반환
    '''
    def filter_valid(self, messages):
        messages_to_delete = []
        messages_to_handle = []
        headers = {
            'token': self.token,
            'Content-Type': 'application/json'
        }
        for message in messages:
            endpoint = os.path.join(self.base_url, f"inferences/{self.api_id}/evaluate/id-poll/{message['id']}")
            with requests.Session() as s:
                # backoff time = backoff_factor * (2 ** (retry_number - 1)) (단, retry_number = 1일 때는 backoff time = 0)
                # 참고 : https://github.com/urllib3/urllib3/blob/745b002e3476f6c4ab707a2b1c82875038249be0/src/urllib3/util/retry.py#L296
                retries = Retry(total=self.max_retry, backoff_factor=0.05, status_forcelist=[ 500, 502, 503, 504 ])
                adapter = HTTPAdapter(max_retries=retries)
                s.mount('http://', adapter)
                s.mount('https://', adapter)
                response = s.get(endpoint, headers = headers)
                if response.status_code == 200:
                    messages_to_handle.append(message)
                elif response.status_code < 500: # 400대 에러일 때는 확실히 유효하지 않은 메세지로 판단
                    logger.warning(f'error from check message validation / response status_code {response.status_code}: {response.text} \n poll function will return None.', event = Event.POLL)
                    messages_to_delete.append(message)
                else: # 5회 재시도해도 500대 에러일 때는 유효한지 알 수 없으므로 유효하지 않은 메세지로 판단
                    logger.error(f'error from check message validation / response status_code {response.status_code}: {response.text} \n poll function will return None.', event = Event.POLL)
                    messages_to_handle.append(message)
        try:
            if (len(messages_to_delete) > 0):
                self.delete_messages(list(map(lambda x: x['id'], messages_to_delete)))
                logger.info(
                    message = f"Deleted {len(messages_to_delete)} invalid messages: {messages_to_delete}"
                )
            return messages_to_handle
        except Exception as e:
            logger.error(f"Error while validating evaluate message\n{e}", event = Event.POLL)

    def poll(self, max_number_of_messages = 1, mock=True):
        if get_shutdown_requested():
            logger.info(
                "System shutdown gracefully",
                event = Event.SHUTDOWN
            )
            sys.exit(0)
        if not isinstance(max_number_of_messages,int): TypeError("max_number_of_messages is not a int")
        if not isinstance(mock, bool): TypeError("mock is not a bool")
        if mock:
            logger.info(
                "return mock",
                data = self.mock
            )
            return self.mock
        
        if self.use_sqs:
            response = self.sqs.receive_message(
                QueueUrl = self.queue_url,
                MaxNumberOfMessages = max_number_of_messages,  # 가져올 메시지의 최대 수 (1개 이상 설정 가능)
                WaitTimeSeconds = 0       # 긴 폴링을 위한 대기 시간 (초 단위)
            )
            ret = []
            messages = response.get('Messages', [])
            for message in messages:
                message_body = message['Body']
                try:
                    # message_body를 딕셔너리로 변환
                    message_dict = json.loads(message_body)
                except json.JSONDecodeError:
                    logger.error("유효한 JSON 형식이 아닙니다.")
                self.evaluates[message_dict['id']] = message['ReceiptHandle']
                ret.append(message_dict)
            
            ret = self.filter_valid(ret)
            if len(ret) == 0:
                return None
            elif len(ret) == 1:
                logger.info(
                    message = "return sqs item",
                    event = Event.POLL,
                    data = ret[0]
                )
                set_context_evaluate(
                    evaluate_id=ret[0]['id'],
                    account_id=ret[0]['accountId']
                )
                self.poll_time = time.time()
                return ret[0]
            else:
                logger.info(
                    message = f"return sqs item: {ret}",
                    event = Event.POLL,
                    data = ret
                )
                self.poll_time = time.time()
                return ret

        time.sleep(0.2)
        url = f"{self.evaluate_url}/poll"

        headers = {
        'token': self.token
        }
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 422:
            return None
        elif response.status_code != 200:
            logger.warning(f'error from poll / response status_code {response.status_code}: {response.text} \n poll function will return None.')
            return None
        logger.info(
            message = "return poll item",
            event = Event.POLL,
            data = response.json()
        )
        set_context_evaluate(
            evaluate_id=response.json()['id'],
            account_id=response.json()['accountId']
        )
        self.poll_time = time.time()
        return response.json()
        
    def validate(self, evaluate_id, output, mock=True, log=True, inference_time=None):
        try:
            if mock:
                logger.debug(output)
                return
            if inference_time == None and self.poll_time != None:
                inference_time = time.time() - self.poll_time
                self.poll_time = None
            if self.use_sqs:
                try: 
                    response = self.sqs.delete_message(
                        QueueUrl = self.queue_url,
                        ReceiptHandle = self.evaluates[evaluate_id]
                    )
                except Exception as e:
                    logger.error(f"error from sqs.delete_message\n{e}")
                    del self.evaluates[evaluate_id]

            payload = json.dumps({
                "id": evaluate_id,
                "json": output
            })

            url = f"{self.evaluate_url}/validate"

            headers = {
                'token': self.token,
                'Content-Type': 'application/json'
            }

            if log:
                logger.info(
                    message = "validate payload",
                    event = Event.VALIDATE,
                    properties = {
                        "evaluate_id": evaluate_id,
                        "inference_time": inference_time,
                    },
                    data = output
                )
            with requests.Session() as s:
                retries = Retry(total=self.max_retry, backoff_factor=0.05, status_forcelist=[ 500, 502, 503, 504 ])
                adapter = HTTPAdapter(max_retries=retries)
                s.mount('http://', adapter)
                s.mount('https://', adapter)
                response = s.put(url, headers=headers, data=payload)
                if response.status_code == 200:
                    return
                else:
                    message = f'error from validate / response status_code {response.status_code}: {response.text}'
                    sentry_sdk.capture_message(message)
                    raise Exception(message)
        finally:
            clear_context_evaluate()
        
    def validate_error(self, evaluate_id, output, mock=True):
        try:
            if not isinstance(evaluate_id, int): raise TypeError('evaluate_id is not a int')
            if not isinstance(output, dict): raise TypeError('output is not a dict')
            if not isinstance(mock, bool): raise TypeError('mock is not a bool')
            try:
                payload = json.dumps({
                    "id": evaluate_id,
                    "json": output
                })
            except Exception as e:
                Exception("failed to parse validate_error input : ", e)
            if mock:
                logger.debug(output)
                return

            if self.use_sqs:
                try: 
                    response = self.sqs.delete_message(
                        QueueUrl = self.queue_url,
                        ReceiptHandle = self.evaluates[evaluate_id]
                    )
                except Exception as e:
                    logger.error(f"error from sqs.delete_message\n{e}")
                    del self.evaluates[evaluate_id]

            payload = json.dumps({
                "id": evaluate_id,
                "error": output
            })

            url = f"{self.evaluate_url}/error"

            headers = {
                'token': self.token,
                'Content-Type': 'application/json'
            }

            logger.info(
                message = "validate_error payload",
                event = Event.VALIDATE_ERROR,
                properties = {
                    "evaluate_id": evaluate_id,
                },
                data = output
            )

            with requests.Session() as s:
                retries = Retry(total=self.max_retry, backoff_factor=0.05, status_forcelist=[ 500, 502, 503, 504 ])
                adapter = HTTPAdapter(max_retries=retries)
                s.mount('http://', adapter)
                s.mount('https://', adapter)
                response = s.put(url, headers=headers, data=payload)
                if response.status_code == 200:
                    return
                else:
                    message = f'error from validate_error / response status_code {response.status_code}: {response.text}'
                    sentry_sdk.capture_message(message)
                    raise Exception(message)
        finally:
            clear_context_evaluate()
        
    def download_from_url(self, url):
        r = requests.get(url, stream=True)
        if r.status_code != 200:
            raise Exception(f"can't download from url {r.status_code} : {r.text}")
        else:
            return io.BytesIO(r.content)
            # return Image.open(io.BytesIO(r.content)).convert('RGB')

    def download_from_s3(self, bucket, key, download_path):
        try:
            self.s3.download_file(bucket, key, download_path)
        except Exception as e:
            raise Exception(f"failed to download from s3\n{e}")

    def upload_s3(self, upload_path, bucket, key = None, account_id = None):
        if key is None and account_id is not None:
            if not isinstance(account_id, int): raise TypeError('account_id is not a int')
            key = f"channel_id={account_id}/{time.strftime('y=%Y/m=%m/d=%d', time.localtime(time.time()))}/{os.path.basename(upload_path)}"
        try:
            self.s3.upload_file(upload_path, bucket, key)
            logger.info(
                message = "uploaded to s3://{bucket}/{key}",
                event = Event.UPLOAD_S3,
            )
            return os.path.join(f"https://{bucket}.s3.ap-northeast-2.amazonaws.com", key)
        except Exception as e:
            raise Exception(f"failed to upload s3\n{e}")

    def stop_instance(self):
        try:
            res = requests.request("GET", 'http://169.254.169.254/latest/meta-data/instance-id')
            if res.status_code != 200:
                raise Exception("get instance-id failed!")
            instance_id = res.text[2:]
            
            url = f"https://api.dalpha.so/instances/{instance_id}/stop/@sdk"

            headers = {
                'token': self.token,
                'Content-Type': 'application/json'
            }

            response = requests.request("PUT", url, headers=headers)
            if response.status_code != 200:
                raise Exception(f'error from stop_instance / response status_code {response.status_code}')

        except Exception as e:
            raise Exception(f"error from stop_instance\n{e}")