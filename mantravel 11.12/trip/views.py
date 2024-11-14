from third_service.kimi_api import multi_turn_chat
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db import transaction
from .models import destination
import  re


@csrf_exempt  # 禁用 CSRF 验证，适用于 POST 请求
def kimi_chat_view(request):
    if request.method == "POST":
        # 获取用户传入的 URL，如果没有传入则返回错误信息
        query_url = request.POST.get("url")
        if not query_url:
            return JsonResponse({"error": "URL 参数是必需的"}, status=400)
        # 调用 multi_turn_chat 函数，传入用户提供的 URL
        response, history = multi_turn_chat(query_url)
        return HttpResponse(response)


@csrf_exempt
def mysql_test(request):
    # 定义 response 数据
    response = """
    <q>
    ‘鼓浪屿’(景点)：厦门的标志性景点，适合夏季避暑，需提前购买船票并注意防晒，  
    ‘厦门大学’(景点)：著名学府，周边有白城沙滩和南普陀寺等景点，  
    ‘曾厝垵’(美食)：美食聚集地，有沙茶面、炸五香、烤生蚝等厦门特色小吃，  
    ‘植物园’(景点)：适合植物爱好者，人多时体验感不佳，  
    ‘八市’(美食)：海鲜爱好者的天堂，新鲜且性价比高的海鲜大排档，  
    ‘沙坡尾’(景点)：适合拍照打卡，有很多摄影师提供免费拍照服务，  
    ‘中山路’(美食)：购物和美食的好去处，靠近厦门大学，  
    ‘珍珠湾’(景点)：适合看日出日落和海景，  
    ‘黄厝’(景点)：适合看日出日落，靠近海边，  
    ‘八市’(美食)：海鲜市场，新鲜且性价比高的海鲜，   
    </q>

    旅游规划：
    <travel>
    第一天：
    1：鼓浪屿
    2：厦门大学
    3：曾厝垵
    4：沙坡尾

    第二天：
    1：植物园
    2：八市
    3：中山路
    4：珍珠湾
    </travel>
    """

    # 使用正则表达式提取地名、标签（景点、美食等）和描述
    destinations = re.findall(r"‘(.+?)’\((.+?)\)：(.*?)(?=‘|</q>)", response, re.DOTALL)

    # 将提取的数据存储到数据库
    try:
        with transaction.atomic():  # 确保数据库操作的原子性
            for name, tag, description in destinations:
                # 使用 update_or_create 方法插入或更新记录
                destination.objects.update_or_create(
                    name=name,  # 查询条件：根据 name 字段匹配
                    defaults={
                        'tag': tag,
                        'description': description
                    }
                )
        return HttpResponse("Data stored successfully", content_type="text/plain")
    except Exception as e:
        print("Database insertion error:", e)
        return JsonResponse({"error": f"Failed to insert data: {e}"}, status=500)