from rest_framework import viewsets
from .models import Memo
from .serializers import MemoSerializer

class MemoViewSet(viewsets.ModelViewSet):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer

    def create(self, request, *args, **kwargs):
        print("Received request:", request.data)  # 添加调试信息
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        print("Updating memo:", request.data)  # 添加调试信息
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        print("Deleting memo with id:", kwargs['pk'])  # 添加调试信息
        return super().destroy(request, *args, **kwargs)