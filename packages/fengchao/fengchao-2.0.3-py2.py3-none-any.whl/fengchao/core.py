# -*- coding:utf-8 -*-
"""
# File       : core.py
# Time       ：2024/2/23 13:40
# Author     ：andy
# version    ：python 3.9
"""
import json
import sys
import uuid
from typing import Union, Generator, Optional
from urllib.parse import urljoin

import requests
from loguru import logger
from tenacity import retry, stop_after_attempt

from .comments import Comments
from .protocol import ModelCard, ModelList, FinalResponse, PromptCard, PromptList, KGList, KGCard, \
    ChatCompletionResponseChoice, ChatMessage, ChatCompletionResponseUsage, ChatCompletionResponse
from .utils import create_token, Retry


class Base:
    def __init__(self, api_key: str, secret_key: str, base_url: str, logger_level: str):
        """
        初始化
        :param api_key:
        :param secret_key:
        :param base_url: 基础请求地址
        :param logger_level: 设置日志输出级别，可选：DEBUG，INFO，WARNING，ERROR，CRITICAL
        """
        logger.remove()
        self.logger = logger.add(sys.stderr, level=logger_level)
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url

    def do(self, method, url, payload=None, headers=None, stream=False) -> requests.Response:
        """
        请求远程服务，默认失败进行重试
        :param method:
        :param url:
        :param payload:
        :param headers:
        :param stream:
        :return:
        """
        _retry = retry(stop=stop_after_attempt(Comments.RETRY.retry_num), before=Comments.RETRY.before,
                       after=Comments.RETRY.after, before_sleep=Comments.RETRY.before_sleep)

        @_retry
        def _do():
            path_url = urljoin(self.base_url, url)
            response = requests.request(method, path_url, json=payload, headers=headers, stream=stream, timeout=Comments.TIMEOUT)
            return response
        return _do()

    def models(self) -> FinalResponse:
        """
        查看支持的模型列表
        :return:
        """
        headers = {
            "content-type": "application/json"
        }
        try:
            response = self.do("GET", Comments.MODELS_URL, headers=headers)
        except Exception as e:
            logger.error("查看模型列表服务异常：{}".format(e.__str__()))
            return FinalResponse(status=400, msg="接口异常：{}".format(e.__str__()))
        if response.status_code == 200:
            model = json.loads(response.text)
            model_card = [ModelCard(id=m.get('id'), owned_by=m.get('owned_by'), mode=m.get('mode'),
                                    price=m.get('price'), unit=m.get('unit'), max_input_token=m.get('max_input_token'),
                                    max_output_token=m.get('max_output_token'),channel=m.get('channel')) for m in model['data']]
            return FinalResponse(data=ModelList(data=model_card))
        else:
            return FinalResponse(status=response.status_code, msg=response.text)

    def prompts(self) -> FinalResponse:
        """
        查看支持的指令列表
        :return:
        """
        headers = {
            "content-type": "application/json"
        }
        try:
            response = self.do("GET", Comments.PROMPTS_URL, headers=headers)
        except Exception as e:
            logger.error("查看指令列表服务异常：{}".format(e.__str__()))
            return FinalResponse(status=400, msg="接口异常：{}".format(e.__str__()))
        if response.status_code == 200:
            prompt = json.loads(response.text)
            prompt_card = [PromptCard(id=p.get('id'), prefix=p.get('prefix'), prompt=p.get('prompt'),
                                    system=p.get('system')) for p in prompt['data']]
            return FinalResponse(data=PromptList(data=prompt_card))
        else:
            return FinalResponse(status=response.status_code, msg=response.text)

    def kgs(self) -> FinalResponse:
        """
        查看支持的知识库列表
        :return:
        """
        headers = {
            "content-type": "application/json"
        }
        try:
            response = self.do("GET", Comments.KGS_URL, headers=headers)
        except Exception as e:
            logger.error("查看知识库列表服务异常：{}".format(e.__str__()))
            return FinalResponse(status=400, msg="接口异常：{}".format(e.__str__()))
        if response.status_code == 200:
            kg = json.loads(response.text)
            kg_card = [KGCard(id=k.get('id'), desc=k.get('desc')) for k in kg['data']]
            return FinalResponse(data=KGList(data=kg_card))
        else:
            return FinalResponse(status=response.status_code, msg=response.text)

    def check_model_channel(self, model):
        """
        检查模型类型
        :param model:
        :return:
        """
        model_list = self.models()
        if model_list.status == 200:
            for model_card in model_list.data.data:
                if model_card.id == model:
                    return model_card.channel
        return None

    @staticmethod
    def prepare_chat_result(response):
        """
        格式化结果
        :param response:
        :return:
        """
        choices = ChatCompletionResponseChoice(
            index=response['choices'][0]['index'],
            message=ChatMessage(role=response['choices'][0]['message']['role'],
                                content=response['choices'][0]['message']['content']),
            finish_reason=response['choices'][0]['finish_reason']
        )
        usage = ChatCompletionResponseUsage(
            prompt_tokens=response['usage']['prompt_tokens'],
            completion_tokens=response['usage']['completion_tokens'],
            total_tokens=response['usage']['total_tokens']
        )
        chunk = ChatCompletionResponse(request_id=response['request_id'], model=response['model'], choices=[choices],
                                       usage=usage, status=200, msg="执行成功", knowledge=response['knowledge'])
        return chunk

    def invoke_chat(self, url:str, headers:dict, payload:dict) -> FinalResponse:
        """
        同步请求
        :param url: 请求地址
        :param headers: 请求头
        :param payload: 请求参数
        :return:
        """
        try:
            response = self.do("POST", url, payload=payload, headers=headers)
        except Exception as e:
            logger.error("同步接口服务异常：{}".format(e.__str__()))
            return FinalResponse(status=400, msg="接口异常：{}".format(e.__str__()))
        if response.status_code == 200:  # 请求正常
            result = json.loads(response.text)
            if result['status'] == 200:  # 响应正常
                result = self.prepare_chat_result(result)
                return FinalResponse(data=result)
            else:  # 响应异常
                return FinalResponse(status=result['status'], msg=result['msg'])
        else:  # 请求异常
            return FinalResponse(status=response.status_code, msg=response.text)

    def async_invoke_chat(self, url:str, headers:dict, payload:dict) -> FinalResponse:
        """
        异步请求
        :param url: 请求地址
        :param headers: 请求头
        :param payload: 请求参数
        :return:
        """
        try:
            response = self.do("POST", url, payload=payload, headers=headers)
        except Exception as e:
            logger.error("异步结果服务异常：{}".format(e.__str__()))
            return FinalResponse(status=400, msg="接口异常：{}".format(e.__str__()))
        if response.status_code == 200:  # 请求正常
            result = json.loads(response.text)
            if result['status'] == 200:  # 响应正常
                return FinalResponse(data=result['choices'][0]['message']['content'])
            else:  # 响应异常
                return FinalResponse(status=result['status'], msg=result['msg'])
        else:  # 请求异常
            return FinalResponse(status=response.status_code, msg=response.text)

    def sse_chat(self, url:str, headers:dict, payload:dict) -> Generator:
        """
        同步请求
        :param url: 请求地址
        :param headers: 请求头
        :param payload: 请求参数
        :return:
        """
        try:
            response = self.do("POST", url, payload=payload, headers=headers, stream=True)
        except Exception as e:
            logger.error("流式服务异常：{}".format(e.__str__()))
            yield FinalResponse(status=400, msg="接口异常：{}".format(e.__str__()))
        else:
            if response.status_code == 200: # 请求正常
                for chunk in response.iter_lines(decode_unicode=True):
                    if chunk.startswith(":") or not chunk:
                        continue
                    field, _p, value = chunk.partition(":")
                    if field == "data":
                        result = json.loads(value)
                        if result['status'] == 200: # 响应正常
                            result = self.prepare_chat_result(result)
                            yield FinalResponse(data=result)
                        else: # 响应异常
                            yield FinalResponse(status=result['status'], msg=result['msg'])
            else: # 请求异常
                yield FinalResponse(status=response.status_code, msg=response.text)

    def prepare_args(self, model, query ,request_id ,system, prompt ,is_sensitive, task_id,
                           history, do_sample ,temperature, top_p, max_tokens, mode, knowledge,
                           top_k, threshold, try_num, timeout, retry_action):
        token = create_token(self.api_key, self.secret_key)
        if timeout is not None:
            Comments.TIMEOUT = timeout
        if try_num is not None:
            Comments.RETRY.retry_num = try_num
        if history is None:
            history = []
        if request_id is None:
            request_id = uuid.uuid1().__str__()
        if retry_action is not None:
            Comments.RETRY = retry_action
        if mode == 'async_result' and task_id is None: raise ValueError("task_id不能为空")
        headers = {
            "content-type": "application/json",
            "Authorization": token
        }
        payload = {
            'model': model,
            'query': query,
            'request_id': request_id,
            'system': system,
            'prompt': prompt,
            'is_sensitive': is_sensitive,
            'task_id': task_id,
            'history': history,
            'do_sample': do_sample,
            'temperature': temperature,
            'top_p': top_p,
            'max_tokens': max_tokens,
            'knowledge': knowledge,
            'top_k': top_k,
            'threshold': threshold,
            'mode': mode
        }
        url = Comments.LOCAL_URL if self.check_model_channel(model) == "本地模型" else Comments.ONLINE_URL
        return headers, payload, url


class FengChao(Base):
    def __init__(self, api_key: str, secret_key: str, base_url: str = Comments.BASE_URL, logger_level: str = 'INFO'):
        """
        初始化
        :param api_key:
        :param secret_key:
        :param base_url: 基础请求地址
        :param logger_level: 设置日志输出级别，可选：DEBUG，INFO，WARNING，ERROR，CRITICAL
        """
        super().__init__(api_key, secret_key, base_url, logger_level)


    def chat(self,
             model: str,
             query: Optional[str] = None,
             request_id: Optional[str] = None,
             system: Optional[str]=None,
             prompt: Optional[str]=None,
             is_sensitive: bool=True,
             task_id: Optional[str]=None,
             history: Optional[list]=None,
             do_sample: bool=True,
             temperature: float =0.8,
             top_p: float =0.75,
             max_tokens: int =256,
             mode: str ='invoke',
             knowledge: Optional[str]=None,
             top_k: int =5,
             threshold: int=500,
             try_num: Optional[int] = None,
             timeout: Optional[int] = None,
             retry_action: Optional[Retry] = None) -> Union[FinalResponse, Generator]:
        """
        创建对话服务
        :param model: 选择模型，具体查看models()函数
        :param query: 请求问题
        :param request_id: 请求ID
        :param system: 系统描述信息
        :param prompt: 指令描述信息
        :param is_sensitive: 是否过滤敏感词，默认：True
        :param task_id: 异步请求返回的任务ID
        :param history: 历史对话数据
        :param do_sample: 是否进行采样，默认：True
        :param temperature: 温度，默认：0.8
        :param top_p: 默认：0.75
        :param max_tokens: 最大输出长度。默认：256
        :param mode: 选择对话模式，同步：invoke，异步：async，异步结果：async_result，流式：stream。默认：invoke
        :param knowledge: 选择要使用的知识库，默认：None
        :param top_k: 知识库参数，命中知识数量
        :param threshold: 知识库参数，阈值，数值范围约为0-1100，如果为0，则不生效，经测试设置为小于500时，匹配结果更精准
        :param try_num: 请求失败重试次数，默认：3
        :param timeout: 请求超时时间，单位秒，默认：600
        :param retry_action: 自定义重试操作行为，需继承Retry类，重写其中的方法
        :return:
        """
        headers, payload, url = self.prepare_args(model, query ,request_id ,system, prompt ,is_sensitive, task_id,
                                                history, do_sample ,temperature, top_p, max_tokens, mode, knowledge,
                                                top_k, threshold, try_num, timeout, retry_action)
        if mode == 'invoke':
            return self.invoke_chat(url, headers, payload)
        elif mode == 'async':
            return self.async_invoke_chat(url, headers, payload)
        elif mode == 'async_result':
            return self.invoke_chat(url, headers, payload)
        elif mode == 'stream':
            return self.sse_chat(url, headers, payload)
        else:
            raise "{}不支持的模式".format(mode)


class FengChaoAsync(Base):
    def __init__(self, api_key: str, secret_key: str, base_url: str = Comments.BASE_URL, logger_level: str = 'INFO'):
        """
        初始化
        :param api_key:
        :param secret_key:
        :param base_url: 基础请求地址
        :param logger_level: 设置日志输出级别，可选：DEBUG，INFO，WARNING，ERROR，CRITICAL
        """
        super().__init__(api_key, secret_key, base_url, logger_level)

    async def invoke_chat(self, url:str, headers:dict, payload:dict) -> FinalResponse:
        return super().invoke_chat(url, headers, payload)

    async def async_invoke_chat(self, url:str, headers:dict, payload:dict) -> FinalResponse:
        return super().async_invoke_chat(url, headers, payload)

    async def sse_chat(self, url:str, headers:dict, payload:dict) -> Generator:
        return super().sse_chat(url, headers, payload)

    async def chat(self,
             model: str,
             query: Optional[str] = None,
             request_id: Optional[str] = None,
             system: Optional[str]=None,
             prompt: Optional[str]=None,
             is_sensitive: bool=True,
             task_id: Optional[str]=None,
             history: Optional[list]=None,
             do_sample: bool=True,
             temperature: float =0.8,
             top_p: float =0.75,
             max_tokens: int =256,
             mode: str ='invoke',
             knowledge: Optional[str]=None,
             top_k: int =5,
             threshold: int=500,
             try_num: Optional[int] = None,
             timeout: Optional[int] = None,
             retry_action: Optional[Retry] = None) -> Union[FinalResponse, Generator]:
        """
        创建对话服务
        :param model: 选择模型，具体查看models()函数
        :param query: 请求问题
        :param request_id: 请求ID
        :param system: 系统描述信息
        :param prompt: 指令描述信息
        :param is_sensitive: 是否过滤敏感词，默认：True
        :param task_id: 异步请求返回的任务ID
        :param history: 历史对话数据
        :param do_sample: 是否进行采样，默认：True
        :param temperature: 温度，默认：0.8
        :param top_p: 默认：0.75
        :param max_tokens: 最大输出长度。默认：256
        :param mode: 选择对话模式，同步：invoke，异步：async，异步结果：async_result，流式：stream。默认：invoke
        :param knowledge: 选择要使用的知识库，默认：None
        :param top_k: 知识库参数，命中知识数量
        :param threshold: 知识库参数，阈值，数值范围约为0-1100，如果为0，则不生效，经测试设置为小于500时，匹配结果更精准
        :param try_num: 请求失败重试次数，默认：3
        :param timeout: 请求超时时间，单位秒，默认：600
        :param retry_action: 自定义重试操作行为，需继承Retry类，重写其中的方法
        :return:
        """
        headers, payload, url = self.prepare_args(model, query, request_id, system, prompt, is_sensitive, task_id,
                                                  history, do_sample, temperature, top_p, max_tokens, mode, knowledge,
                                                  top_k, threshold, try_num, timeout, retry_action)
        if mode == 'invoke':
            result = await self.invoke_chat(url, headers, payload)
            return result
        elif mode == 'async':
            result = await self.async_invoke_chat(url, headers, payload)
            return result
        elif mode == 'async_result':
            result = await self.invoke_chat(url, headers, payload)
            return result
        elif mode == 'stream':
            result = await self.sse_chat(url, headers, payload)
            return result
        else:
            raise "{}不支持的模式".format(mode)