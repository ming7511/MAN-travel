from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import generate_verification_code, verify_code  # 引入上面的验证码生成和验证函数

User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        code = generate_verification_code(phone)
        return Response({"message": "Verification code sent", "code": code}, status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        code = request.data.get('code')

        if verify_code(phone, code):
            user, created = User.objects.get_or_create(phone=phone)

            if created:
                user.set_unusable_password()  # 如果自动注册用户，设一个不可用密码

            # 生成并返回 JWT token
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)
