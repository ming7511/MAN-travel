from third_service.kimi_api import multi_turn_chat
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


@csrf_exempt  # 禁用 CSRF 验证，适用于 POST 请求
def kimi_chat_view(request):
    if request.method == "POST":
        # 获取用户传入的 URL，如果没有传入则返回错误信息
        query_url = request.POST.get("url")
        if not query_url:
            return JsonResponse({"error": "URL 参数是必需的"}, status=400)
        # 调用 multi_turn_chat 函数，传入用户提供的 URL
        response, history = multi_turn_chat(query_url)
        # 返回响应结果
        return HttpResponse(response, content_type="text/plain")
    else:
        return JsonResponse({"error": "仅支持 POST 请求"}, status=405)