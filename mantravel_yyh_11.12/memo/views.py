from rest_framework import viewsets
from .models import Memo
from .serializers import MemoSerializer
# Create your views here.


class MemoViewSet(viewsets.ModelViewSet):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer

    def create(self, request, *args, **kwargs):
        print("Received request:", request.data)  # 添加调试信息
        return super().create(request, *args, **kwargs)