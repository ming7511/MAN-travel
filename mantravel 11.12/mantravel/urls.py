
from trip.views import kimi_chat_view
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
# 定义一个简单的视图函数作为根路径
def home(request):
    return HttpResponse("Welcome to the homepage!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/trip/', include('trip.urls')),
    path('api/accounts/', include('accounts.urls')),  # 包含 accounts 应用的路由
    path('', home),  # 根路径配置
]
