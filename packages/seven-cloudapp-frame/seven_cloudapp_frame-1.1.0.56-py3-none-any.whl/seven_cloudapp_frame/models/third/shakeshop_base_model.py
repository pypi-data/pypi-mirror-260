# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2022-01-10 11:31:34
@LastEditTime: 2024-02-22 15:37:02
@LastEditors: HuangJianYi
@Description: 抖店接口业务模型
"""

import json
import time
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import MD5, SHA256, Hash
from cryptography.hazmat.primitives.hmac import HMAC
from seven_cloudapp_frame.libs.customize.seven_helper import SevenHelper
from seven_cloudapp_frame.models.seven_model import *
from seven_framework.base_model import *


class ShakeShopBaseModel():
    """
    :description: 抖店接口业务模型(IP白名单功能说明应用IP白名单功能:开发者需在开放平台控制台提前配置可信的1P白名单，只有属于1P白名单中的IP地址访问AP接口时，平台网关才允许通过，否则调用AP 接口将被拒绝)
    """
    def __init__(self, context, app_key: str, app_secret: str, app_type, code=None, shop_id: str = None, auth_subject_type: str = None, proxy: str = None, test_mode=False, logging_error=None, logging_info=None):
        """
        :description:  初始化实例，自用型应用传入shop_id用于初始化access token，工具型应用传入code换取access token（如初始化时未传入，可以在访问抖店API之前调用init_token(code)进行token的初始化。
        :param context: 上下文
        :param app_key: app_key
        :param app_secret: app_secret
        :param app_secret: app_secret
        :param app_type: app_type(SELF或TOOL)
        :param code: code
        :param shop_id: 店铺ID
        :param auth_subject_type:授权主体类型，配合auth_id字段使用，YunCang -云仓；WuLiuShang -物流商；WLGongYingShang -物流供应商；MiniApp -小程序；MCN-联盟MCN机构；DouKe-联盟抖客 ；Colonel-联盟团长；
        :param proxy: 代理
        :param test_mode: 是否测试沙盒
        :param logging_error: logging_error
        :param logging_info: logging_info
        :return 
        :last_editors: HuangJianYi
        """
        self.context = context
        self.logging_link_error = logging_error
        self.logging_link_info = logging_info
        self.app_key = app_key
        self.app_secret = app_secret
        self.app_type = app_type
        if self.app_type == "SELF" and not shop_id:
            raise Exception('shop_id不能为空')
        self.shop_id = shop_id
        self.auth_subject_type = auth_subject_type
        self.proxy = proxy
        self.test_mode = test_mode
        if self.test_mode:
            self._gate_way = 'https://openapi-sandbox.jinritemai.com'
        else:
            self._gate_way = 'https://openapi-fxg.jinritemai.com'
        self._version = 2
        redis_token = SevenHelper.redis_init(config_dict=config.get_value("platform_redis")).get(f"shakeshop_access_token:{str(app_key)}_{self.test_mode}")
        if redis_token:
            redis_token = json.loads(redis_token)
        self._token = redis_token
        self._sign_method = 'hmac-sha256'
        if self._token:
            if self._token.get('expires_in') - int(time.time()) < 3000:
                self._refresh_token()
        else:
            if self.app_type == "SELF":
                self.init_token()
            elif self.app_type == "TOOL" and code:
                self.init_token(code)

    def _sign(self, method: str, param_json: str, timestamp: str) -> str:
        param_pattern = 'app_key{}method{}param_json{}timestamp{}v{}'.format(self.app_key, method, param_json, timestamp, self._version)
        sign_pattern = '{}{}{}'.format(self.app_secret, param_pattern, self.app_secret)
        return self._hash_hmac(sign_pattern)

    def _hash_hmac(self, pattern: str) -> str:
        try:
            hmac = HMAC(key=self.app_secret.encode('UTF-8'), algorithm=SHA256(), backend=default_backend())
            hmac.update(pattern.encode('UTF-8'))
            signature = hmac.finalize()
            return signature.hex()
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            return None

    def _access_token(self) -> str:
        """
        :description: 获取access_token
        :return 
        :last_editors: HuangJianYi
        """
        if not self._token:
            raise Exception('no token info, call init_token() to initialize it.')
        try:
            if self._token.get('expires_in') - int(time.time()) < 3000:
                self._refresh_token()
            return self._token.get('access_token')
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            return None

    def init_token(self, code: str = '') -> bool:
        """
        :description: 初始化access_token
        :param code: 工具型应用从授权url回调中获取到的code，自用型应用无需传入。
        :return 
        :last_editors: HuangJianYi
        """
        request_redis_key = f"shakeshop_access_token:{str(self.app_key)}_{self.test_mode}"
        if SevenHelper.is_continue_request(request_redis_key, 2000) == True:
            return False
        try:
            if self.app_type == "TOOL" and not code:
                raise Exception('code不能为空')
            path = '/token/create'
            grant_type = 'authorization_self' if self.app_type == "SELF" else 'authorization_code'
            params = {}
            params.update({'code': code if code else ''})
            params.update({'grant_type': grant_type})
            if self.app_type == "SELF":
                if self.test_mode:
                    params.update({'test_shop': '1'})
                elif self.auth_subject_type:
                    params.update({'auth_subject_type': self.auth_subject_type})
                    params.update({'auth_id': self.shop_id})
                elif self.shop_id:
                    params.update({'shop_id': self.shop_id})
                else:
                    raise Exception('shop_id不能为空')
            result = self._request(path=path, params=params, token_request=True)
            SevenHelper.redis_init().delete(request_redis_key)
            if result and result.get('code') == 10000 and result.get('data'):
                self._token = result.get('data')
                self._token.update({'expires_in': int(time.time()) + result.get('data').get('expires_in')})
                SevenHelper.redis_init(config_dict=config.get_value("platform_redis")).set(f"shakeshop_access_token:{str(self.app_key )}_{self.test_mode}", json.dumps(self._token), ex=3600)
                return True
            else:
                raise Exception("初始化失败：" + json.dumps(result))
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
        return False

    def _get_refresh_token(self) -> str:
        """
        :description: 获取refresh_token
        :return 
        :last_editors: HuangJianYi
        """
        if not self._token:
            return None
        try:
            return self._token.get('refresh_token')
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            return None

    def _refresh_token(self) -> None:
        """
        :description: 刷新refresh_token
        :return 
        :last_editors: HuangJianYi
        """
        request_redis_key = f"shakeshop_access_token:{str(self.app_key)}_{self.test_mode}"
        if SevenHelper.is_continue_request(request_redis_key, 2000) == True:
            return False
        path = '/token/refresh'
        refresh_token = self._get_refresh_token()
        grant_type = 'refresh_token'
        params = {}
        params.update({'grant_type': grant_type})
        params.update({'refresh_token': refresh_token})
        result = self._request(path=path, params=params, token_request=True)
        SevenHelper.redis_init().delete(request_redis_key)
        if result and result.get('err_no') == 0 and result.get('data'):
            self._token = result.get('data')
            self._token.update({'expires_in': int(time.time()) + result.get('data').get('expires_in')})
            SevenHelper.redis_init(config_dict=config.get_value("platform_redis")).set(f"shakeshop_access_token:{str(self.app_key )}_{self.test_mode}", json.dumps(self._token), ex=3600)

    def _request(self, path: str, params: dict, token_request: bool = False, is_log: bool = False) -> json:
        """
        :description: 发起请求
        :param path: api地址
        :param params: 参数集合
        :param token_request: 是否token请求
        :param is_log: 是否记录日志
        :return 
        :last_editors: HuangJianYi
        """
        try:
            headers = {}
            headers.update({'Content-Type': 'application/json'})
            headers.update({'Accept': 'application/json'})
            headers.update({'User-Agent': 'newfire doudian python sdk(https://github.com/minibear2021/doudian)'})
            timestamp = SevenHelper.get_now_datetime()
            param_json = json.dumps(params, sort_keys=True, separators=(',', ':'))
            method = path[1:].replace('/', '.')
            sign = self._sign(method=method, param_json=param_json, timestamp=timestamp)
            if token_request:
                url = self._gate_way + '{}?app_key={}&method={}&param_json={}&timestamp={}&v={}&sign_method={}&sign={}'.format(path, self.app_key, method, param_json, timestamp, self._version, self._sign_method, sign)
            else:
                access_token = self._access_token()
                url = self._gate_way + '{}?app_key={}&method={}&access_token={}&param_json={}&timestamp={}&v={}&sign_method={}&sign={}'.format(path, self.app_key, method, access_token, param_json, timestamp, self._version, self._sign_method, sign)
            log_info = ""
            if is_log == True:
                log_info = f'Request url:{url},Request headers:{headers},Request params:{param_json};'
            response = requests.post(url=url, data=param_json, headers=headers, proxies=self.proxy)
            if is_log == True:
                log_info += f'Response status code: {response.status_code},Response headers:{response.headers},Response content:' + response.content.decode('utf-8')
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)
            if response.status_code != 200:
                return None
            return json.loads(response.content)
        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            return None

    def request(self, path: str, params: dict, is_log: bool = False) -> json:
        """
        :description: 请求抖店API接口
        :param path: 调用的API接口地址，示例：'/material/uploadImageSync'
        :param params: 业务参数字典，示例：{'folder_id':'70031975314169695161250','url':'http://www.demo.com/demo.jpg','material_name':'demo.jpg'}
        :param is_log: 是否记录日志
        :return 
        :last_editors: HuangJianYi
        """
        return self._request(path=path, params=params, is_log=is_log)

    def callback(self, headers: dict, body: bytes, is_log: bool = False) -> json:
        """
        :description: 验证处理消息推送服务收到信息Md5解密模式
        :param headers: headers
        :param body: body
        :param is_log: 是否记录日志
        :return 
        :last_editors: HuangJianYi
        """
        data: str = body.decode('UTF-8')
        if is_log == True:
            if self.context:
                self.context.logging_link_info(f'Callback Header:{headers},Callback Body:{body}')
            elif self.logging_link_info:
                self.logging_link_info(f'Callback Header:{headers},Callback Body:{body}')
        if not data:
            return None
        if headers.get('app-id') != self.app_key:
            return None
        event_sign: str = headers.get('event-sign')
        if not event_sign:
            return None
        h = Hash(algorithm=MD5(), backend=default_backend())
        h.update('{}{}{}'.format(self.app_key, data, self.app_secret).encode('UTF-8'))
        if h.finalize().hex() != event_sign:
            return None
        return json.loads(data)

    def callback_response_success(self):
        """
        :description: 抖店推送服务验证消息，需立即返回success
        :return 字典
        :last_editors: HuangJianYi
        """
        return {'code': 0, 'msg': 'success'}
    
    def callback_response_error(self, error_code: str = 40041, error_message: str = "解析推送数据失败"):
        """
        :description: 抖店推送服务验证消息，需立即返回success
        :param error_code: 错误码
        :param error_message: 错误信息
        :return 字典
        :last_editors: HuangJianYi
        """
        return {'code': error_code, 'message': error_message}

    def build_auth_url(self, service_id: str, state: str) -> str:
        """
        :description: 拼接授权URL，引导商家点击完成授权
        :param service_id: service_id
        :param state: state
        :return
        :last_editors: HuangJianYi
        """
        if self.app_type == "TOOL":
            return 'https://fuwu.jinritemai.com/authorize?service_id={}&state={}'.format(service_id, state)
        else:
            return None
        
    def openid_switch(self, open_id: str, open_id_type: int = 1, is_log=False):
        """
        :description: 提供抖音和抖店 Openid 转换功能(https://op.jinritemai.com/docs/api-docs/162/1973)
        :param open_id: 传入的openId
        :param open_id_type: openId类型，1-抖音openId 2-抖店openId
        :param is_log: 是否记录日志
        :return InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            params = {"open_id": open_id, "open_id_type": open_id_type}
            response = self.request(path="/open/openIdSwitch", params=params, is_log=is_log)
            if response and response.get("code") == 10000 and "data" in response_data:
                response_data = SevenHelper.json_loads(response)
                invoke_result_data.data = response_data["data"] # {"open_id": "dfsdfsgdrwds","open_id_type": "2"}
                return invoke_result_data
            else:
                raise Exception(f"openId转换失败:{SevenHelper.json_dumps(response)}")

        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "openid_switch"
            invoke_result_data.error_message = "抖店接口错误：抖音和抖店Openid转换功能(/open/openIdSwitch)"
            return invoke_result_data

    def get_user_order_list(self, open_id, size=100, page=0, order_status=None, create_time_start=None, create_time_end=None, open_id_type="douyin", is_log=False):
        """
        :description: 支持按抖音小程序open_id查询订单简要信息，仅电商小程序在C端面向用户呈现订单任务类场景使用(https://op.jinritemai.com/docs/api-docs/15/1915)
        :param open_id: 用户openId
        :param size: 单页大小，限制100以内
        :param page: 页码，0页开始
        :param order_status: 订单状态：all-全部，under_sure-待确认，unpaid-待支付，stock_up-待发货，on_delivery-已发货，received-已完成，closed-已关闭，to_groups-待成团
        :param create_time_start: 下单时间：开始，秒级时间戳
        :param create_time_end: 下单时间：截止，秒级时间戳
        :param open_id_type: 用户openId类型，固定为 douyin 抖音
        :param is_log: 是否记录日志
        :return InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            params = {"size": size, "page":page, "open_id":open_id, "open_id_type":open_id_type}
            if order_status:
                params["order_status"] = order_status
            if create_time_start:
                params["create_time_start"] = create_time_start
            if create_time_end:
                params["create_time_end"] = create_time_end

            response = self.request(path="/order/getUserOrderList", params=params, is_log=is_log)
            if response and response.get("code") == 10000 and "data" in response_data:
                response_data = SevenHelper.json_loads(response)
                invoke_result_data.data = response_data["data"]
                return invoke_result_data
            else:
                raise Exception(f"按抖音小程序open_id查询订单简要信息失败:{SevenHelper.json_dumps(response)}")

        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "get_user_order_list"
            invoke_result_data.error_message = "按抖音小程序open_id查询订单简要信息(/order/getUserOrderList)"
            return invoke_result_data   
        
    def order_detail(self, shop_order_id, is_log=False):
        """
        :description: 订单详情查询(https://op.jinritemai.com/docs/api-docs/15/1343)
        :param shop_order_id: 店铺父订单号，抖店平台生成，平台下唯一；
        :param is_log: 是否记录日志
        :return InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            params = {"shop_order_id": shop_order_id}
            response = self.request(path="/order/orderDetail", params=params, is_log=is_log)
            if response and response.get("code") == 10000 and "data" in response_data:
                response_data = SevenHelper.json_loads(response)
                invoke_result_data.data = response_data["data"]
                return invoke_result_data
            else:
                raise Exception(f"订单详情查询失败:{SevenHelper.json_dumps(response)}")

        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "order_detail"
            invoke_result_data.error_message = "抖店接口错误：订单详情查询(/order/orderDetail)"
            return invoke_result_data
        
    def order_search_list(self, page=0, size=100, order_type=None, order_by=None, order_asc=None, product=None, custom_params={}, is_log=False):
        """
        :description: 根据条件检索满足要求的订单列表，支持下单时间和更新时间排序；最大支持查询近90天的数据(https://op.jinritemai.com/docs/api-docs/15/1342)
        :param page: 页码，0页开始
        :param size: 单页大小，限制100以内
        :param order_type: 订单类型 0、普通订单 2、虚拟商品订单 4、电子券（poi核销） 5、三方核销
        :param order_by: 排序条件(create_time 订单创建时间；update_time 订单更新时间；默认create_time；)
        :param order_asc: 排序类型，小到大或大到小，默认大到小
        :param product: 商品，number型代表商品ID，其它代表商品名称
        :param custom_params: 自定义参数字典
        :param is_log: 是否记录日志
        :return InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        try:
            params = {"page": page, "size": size}
            if order_type:
                params["order_type"] = order_type
            if order_by:
                params["order_by"] = order_by
            if order_asc:
                params["order_asc"] = order_asc
            if product:
                params["product"] = product
                
            params.update(custom_params)
            response = self.request(path="/order/searchList", params=params, is_log=is_log)
            if response and response.get("code") == 10000 and "data" in response_data:
                response_data = SevenHelper.json_loads(response)
                invoke_result_data.data = response_data["data"]
                return invoke_result_data
            else:
                raise Exception(f"订单列表查询失败:{SevenHelper.json_dumps(response)}")

        except Exception as e:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "order_search_list"
            invoke_result_data.error_message = "抖店接口错误：订单列表查询(/order/searchList)"
            return invoke_result_data




