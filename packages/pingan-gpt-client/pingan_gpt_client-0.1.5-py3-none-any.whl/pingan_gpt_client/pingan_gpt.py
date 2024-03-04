import logging
import uuid

from datetime import datetime
import binascii
from typing import List, Optional, Dict

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from urllib.parse import urlencode
import requests
# requests的并发版本
import grequests


class PATechGPTClient:

    def __init__(self, api_credential: str, api_private_key: str, app_key: str, secret_key: str, scene_id: str,
                 request_token_url: str = "http://eagw-gateway-sf.paic.com.cn:80/auth/token/apply",
                 dialog_url: str = "http://eagw-gateway-sf.paic.com.cn:80/chatgpt/dialog"):
        # param in eagw
        self.API_CREDENTIAL = api_credential
        self.API_PRIVATE_KEY = api_private_key

        self.REQUEST_TOKEN_URL = request_token_url
        self.DIALOG_URL = dialog_url

        # param in pingan gpt platform
        self.APP_KEY = app_key
        self.APP_SECRET = secret_key
        self.APP_DATA = {
            "appKey": self.APP_KEY,
            "appSecret": self.APP_SECRET
        }
        self.APP_DATA_ENCODE = urlencode(self.APP_DATA)
        self.SCENE_ID = scene_id

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

    def get_headers_for_dialog_api(self) -> Dict[str, str]:
        headers = self.__get_headers_template()
        headers['Content-Type'] = "application/json"
        headers['openApiCode'] = "API026840"
        headers["access_token"] = self.request_token()
        return headers

    def pingan_gpt_inference(self, prompt: str,
                             temperature: float = 0.5,
                             top_p: float = 0.5,
                             session_id: Optional[str] = None,
                             own_history: List[str] = [],
                             max_new_tokens: int = 1000,
                             timeout=120) -> Optional[str]:
        try:
            response = requests.post(self.DIALOG_URL,
                                     headers=self.get_headers_for_dialog_api(),
                                     json={
                                         "prompt": prompt,
                                         "sessionId": session_id if session_id else str(uuid.uuid4()),
                                         "sceneId": self.SCENE_ID,
                                         "isUseOwnHistory": bool(len(own_history)),
                                         "ownHistory": own_history,
                                         "max_new_tokens": max_new_tokens,
                                         "generateParam": {"temperature": temperature, "top_p": top_p}

                                     },
                                     timeout=timeout)
        except Exception as error:
            self.logger.error(error)
            return None

        if response.ok:
            return response.json()
        else:
            self.logger.warning(response.text)
            return None

    def pingan_gpt_batch_inference(self, prompts: List[str],
                                   temperature: float = 0.5,
                                   top_p: float = 0.5,
                                   session_id: str = None,
                                   own_history: List[str] = [],
                                   max_new_tokens: int = 1000,
                                   timeout=120,
                                   concurrent=10) -> List[Optional[str]]:
        try:
            headers = self.get_headers_for_dialog_api()
            rs = [grequests.post(self.DIALOG_URL,
                                 headers=headers,
                                 json={
                                     "prompt": prompt,
                                     "sessionId": session_id if session_id else str(uuid.uuid4()),
                                     "sceneId": self.SCENE_ID,
                                     "isUseOwnHistory": bool(len(own_history)),
                                     "ownHistory": own_history,
                                     "max_new_tokens": max_new_tokens,
                                     "generateParam": {"temperature": temperature, "top_p": top_p}

                                 },
                                 timeout=timeout) for prompt in prompts]
            responses = grequests.map(rs, size=concurrent)
        except Exception as error:
            self.logger.error(error)
            return len(prompts) * [None]
        return [response.json() if response.ok else None for response in responses]
