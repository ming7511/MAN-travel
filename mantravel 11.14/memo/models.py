from django.db import models
from django.conf import settings
from trip.models import TripInformation

class Memo(models.Model):
    STATUS_CHOICES = [
        ('yes', '带了行李'),
        ('no', '没带行李'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # 备忘录名称
    note = models.TextField()  # 备注
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)  # 状态
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    trip_information = models.ForeignKey(TripInformation, on_delete=models.CASCADE, related_name='memos', null=True)  # 添加与 TripInformation 的关联

    def __str__(self):
        return self.name