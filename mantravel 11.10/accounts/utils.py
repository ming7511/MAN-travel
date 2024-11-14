from django.core.cache import cache
import random

def generate_verification_code(phone):
    code = random.randint(1000, 9999)
    cache.set(phone, code, timeout=300)  # 验证码有效期为 5 分钟
    # 发送验证码的逻辑（可以接入短信服务）
    return code

def verify_code(phone, code):
    stored_code = cache.get(phone)
    return str(stored_code) == str(code)
