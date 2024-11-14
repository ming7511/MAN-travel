from django.urls import path
from .views import kimi_chat_view  # 确保 RegisterView 和 LoginView 已经导入

urlpatterns = [
    path('kimi-chat/', kimi_chat_view, name='kimi_chat'),
]
