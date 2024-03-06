import copy
import json
import logging
import uuid

from datetime import datetime
import binascii
from typing import List, Optional, Dict, Any

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from urllib.parse import urlencode
import requests

# requests的并发版本
import warnings
# 消除gevent的告警
from gevent.monkey import MonkeyPatchWarning

warnings.filterwarnings("ignore", category=MonkeyPatchWarning)
import grequests


class PATechGPTClient:

    def __init__(self, api_credential: str, api_private_key: str, app_key: str, secret_key: str, scene_id: str,
                 request_token_url: str = "http://eagw-gateway-sf.paic.com.cn:80/auth/token/apply",
                 dialog_url: str = "http://eagw-gateway-sf.paic.com.cn:80/chatgpt/dialog",
                 dialog_stream_url: str = "http://isps-gpt-gateway-prd-sz.paic.com.cn/chatgpt/dialog/stream"):
        # param in eagw
        self.API_CREDENTIAL = api_credential
        self.API_PRIVATE_KEY = api_private_key

        self.REQUEST_TOKEN_URL = request_token_url
        self.DIALOG_URL = dialog_url
        self.DIALOG_STREAM_URL = dialog_stream_url

        # param in pingan gpt platform
        self.APP_KEY = app_key
        self.APP_SECRET = secret_key
        self.APP_DATA = {
            "appKey": self.APP_KEY,
            "appSecret": self.APP_SECRET
        }
        self.APP_DATA_ENCODE = urlencode(self.APP_DATA)
        self.SCENE_ID = scene_id

        self.STREAM_END = '<eom>'

        self.logger = logging.getLogger(__name__)

    @staticmethod
    def __get_sign(rsa_private_key: str, request_time: str) -> str:
        """
        根据秘钥生成签名
        """
        # 将十六进制字符串转换为二进制字符串
        binary_key = binascii.a2b_hex(rsa_private_key)
        # 创建RSA公钥对象
        pkcs8_private_key = RSA.import_key(binary_key)
        # 注意这里签名用的是requestTime, 务必保证是同一个
        h = SHA256.new(request_time.encode('utf-8'))
        signer = PKCS1_v1_5.new(pkcs8_private_key)
        #  是openApiSignature的值
        signature = signer.sign(h).hex().upper()
        return signature

    def __get_headers_template(self) -> Dict[str, str]:
        request_time = str(int(datetime.now().timestamp() * 1000))
        headers = {
            "X-Auth-Type": "App_Token",
            "openApiCredential": self.API_CREDENTIAL,
            "openApiRequestTime": request_time,
            "openApiSignature": PATechGPTClient.__get_sign(self.API_PRIVATE_KEY, request_time)
        }
        return headers

    def get_headers_for_token_api(self) -> Dict[str, str]:
        headers = self.__get_headers_template()
        headers['Content-Type'] = "application/x-www-form-urlencoded"
        headers['openApiCode'] = "API026878"
        return headers

    def request_token(self) -> Optional[str]:
        response = requests.post(self.REQUEST_TOKEN_URL,
                                 headers=self.get_headers_for_token_api(),
                                 data=self.APP_DATA_ENCODE)
        try:
            '''
            这个判断要比response.status_code == 200 要好。
            只要status_code<400的，response.ok都为True。
            标准来说，post作为create动作时，server应该返回201而不是200。
            碰到转发情况，应该是300系列的状态码。
            '''
            if response.ok:
                return response.json().get("data").get("token")
            else:
                self.logger.warning(response.text)
                return None
        except Exception as error:
            self.logger.error(error)
            return None

    def get_headers_for_dialog_api(self, token: Optional[str] = None) -> Dict[str, str]:
        headers = self.__get_headers_template()
        headers['Content-Type'] = "application/json"
        headers['openApiCode'] = "API026840"
        headers["access_token"] = token if token else self.request_token()
        return headers

    def __payload_template(self,
                           generate_param: Dict[str, Any] = {},
                           session_id: Optional[str] = None,
                           system_instruction: Optional[str] = None,
                           is_use_own_history: Optional[bool] = None,
                           own_history: Optional[List[List[str]]] = None,
                           ) -> Dict[str, Any]:
        payload = {"sessionId": session_id if session_id else str(uuid.uuid4()),
                   "sceneId": self.SCENE_ID,
                   "generateParam": generate_param
                   }
        if system_instruction is not None:
            payload["systemInstruction"] = system_instruction
        if is_use_own_history is not None:
            payload["isUseOwnHistory"] = is_use_own_history
        if own_history is not None:
            payload["ownHistory"] = copy.deepcopy(own_history)
        return payload

    def pingan_gpt_inference(self, prompt: str,
                             generate_param: Dict[str, Any] = {},
                             session_id: Optional[str] = None,
                             system_instruction: Optional[str] = None,
                             is_use_own_history: Optional[bool] = None,
                             own_history: Optional[List[List[str]]] = None,
                             timeout=120, token: Optional[str] = None,
                             only_answer=False, stream=False) -> Optional[str]:

        payload = self.__payload_template(generate_param, session_id, system_instruction, is_use_own_history,
                                          own_history)
        try:
            response = requests.post(self.DIALOG_STREAM_URL if stream else self.DIALOG_URL,
                                     headers=self.get_headers_for_dialog_api(token),
                                     json={"prompt": prompt, **payload},
                                     timeout=timeout, stream=stream)
            if stream:
                for line in response.iter_lines(decode_unicode=True):
                    if only_answer:
                        yield json.loads(line[5:]).get("text")[0]
                    else:
                        yield {"data": json.loads(line[5:])}
            else:
                if response.ok:
                    return response.json().get("data", {}).get("answer") if only_answer else response.json()
                else:
                    self.logger.warning(response.text)
                    return None
        except Exception as error:
            self.logger.error(error)
            return None

    def pingan_gpt_batch_inference(self, prompts: List[str],
                                   generate_param: Dict[str, Any] = {},
                                   session_id: Optional[str] = None,
                                   system_instruction: Optional[str] = None,
                                   is_use_own_history: Optional[bool] = None,
                                   own_history: Optional[List[List[str]]] = None,
                                   timeout=120,
                                   token: Optional[str] = None, only_answer=False,
                                   concurrent=10) -> List[Optional[str]]:

        payload = self.__payload_template(generate_param, session_id, system_instruction, is_use_own_history,
                                          own_history)

        try:
            headers = self.get_headers_for_dialog_api(token)
            rs = [grequests.post(self.DIALOG_URL,
                                 headers=headers,
                                 json={"prompt": prompt, **payload},
                                 timeout=timeout) for prompt in prompts]
            responses = grequests.map(rs, size=concurrent)
        except Exception as error:
            self.logger.error(error)
            return len(prompts) * [None]
        rets = []
        for response in responses:
            if response.ok:
                rets.append(response.json().get("data", {}).get("answer") if only_answer else response.json())
            else:
                rets.append(None)
        return rets

    def is_stream_end(self, text):
        return text == self.STREAM_END
