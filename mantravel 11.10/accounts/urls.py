from django.urls import path
from .views import RegisterView, LoginView  # 确保 RegisterView 和 LoginView 已经导入

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # 注册路径
    path('login/', LoginView.as_view(), name='login'),  # 登录路径
]
