# utils.py

# -*- coding: utf-8 -*-
import os
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from django.core.cache import cache
import random
import logging

# 如果你决定以后使用 .env 文件，可以取消下面两行的注释
# from dotenv import load_dotenv
# load_dotenv()

logger = logging.getLogger(__name__)
logger.info("Testing logging output from utils.py")


def generate_verification_code(phone):
    """
    生成并缓存验证码。验证码有效期为 5 分钟。
    """
    # 生成四位数验证码
    code = random.randint(1000, 9999)

    try:
        # 将验证码存为字符串并存入缓存中，设置过期时间为5分钟
        success = cache.set(phone, str(code), timeout=300)  # 确保验证码存储为字符串

        if success:
            logger.info(f"Successfully stored verification code for {phone}: {code} in cache.")
        else:
            logger.error(f"Failed to store verification code for {phone}: {code} in cache.")
    except Exception as e:
        logger.error(f"Error storing verification code for {phone} in cache: {e}")

    return code


def verify_code(phone, code):
    """
    验证用户输入的验证码是否正确。
    """
    # 从缓存中获取验证码
    stored_code = cache.get(phone)

    # 打印缓存中的验证码，帮助调试
    logger.info(f"Retrieved code from cache for {phone}: {stored_code}")

    if stored_code is None:
        logger.error(f"No verification code found in cache for {phone}.")
        return False

    logger.info(f"Stored code for {phone}: {stored_code}, user provided code: {code}")
    return str(stored_code) == str(code)  # 比较缓存中的验证码和用户输入的验证码


def create_client():
    """
    使用环境变量中的AK&SK初始化账号Client
    @return: Client
    @throws Exception
    """
    access_key_id = os.getenv('ALIYUN_ACCESS_KEY_ID')  # 从环境变量中获取 AccessKey
    access_key_secret = os.getenv('ALIYUN_ACCESS_KEY_SECRET')  # 从环境变量中获取 AccessSecret

    # print(f"Access Key ID: {access_key_id}")  # 调试输出
    # print(f"Access Key Secret: {access_key_secret}")  # 调试输出

    if not access_key_id or not access_key_secret:
        logger.error("AccessKey or AccessSecret is not set in environment variables.")
        raise ValueError("AccessKey or AccessSecret is not set in environment variables.")

    # 打印 AccessKey ID 调试信息（可选，确保不要在生产环境中泄露）
    logger.debug(f"Using AccessKey ID: {access_key_id}")

    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret
    )
    config.endpoint = 'dysmsapi.aliyuncs.com'
    return Dysmsapi20170525Client(config)


def send_sms_code(phone, code):
    client = create_client()
    send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
        sign_name='man游正式版',  # 签名
        template_code='SMS_475265203',  # 模板代码
        phone_numbers=phone,  # 目标手机号
        template_param=f'{{"code":"{code}"}}'  # 短信内容参数
    )
    runtime = util_models.RuntimeOptions()
    try:
        logger.info(f"Sending SMS to {phone} with code {code}")
        response = client.send_sms_with_options(send_sms_request, runtime)
        response_map = response.to_map()
        logger.info(f"Aliyun Response: {response_map}")  # 打印响应
        if response.body.code == 'OK':
            logger.info(f"SMS sent successfully to {phone}")
            return True
        else:
            logger.error(f"Failed to send SMS to {phone}. Response: {response_map}")
            return False
    except Exception as error:
        logger.error(f"Error sending SMS to {phone}: {error}")
        if hasattr(error, 'data') and error.data:
            logger.error(f"Recommend: {error.data.get('Recommend')}")
        return False
