from django.db import models

class TripInformation(models.Model):
    trip_name = models.CharField(max_length=100, verbose_name="想去的地方")
    user_id = models.IntegerField(verbose_name="用户ID")
    start_date = models.DateField(verbose_name="开始日期")
    end_date = models.DateField(verbose_name="结束日期")
    weather_info = models.JSONField(default=dict, verbose_name="天气信息")  # 新增字段

    def __str__(self):
        return self.trip_name

    class Meta:
        verbose_name = "行程信息"
        verbose_name_plural = "行程信息"


class TripPlan(models.Model):
    trip_information = models.ForeignKey(
        TripInformation, on_delete=models.CASCADE, related_name="trip_plans", verbose_name="行程ID"
    )
    days = models.IntegerField(verbose_name="第几天")
    trip_description = models.CharField(max_length=200, verbose_name="目的地")
    trip_order = models.IntegerField(verbose_name="游玩顺序")
    description = models.TextField(verbose_name="目的地简介", blank=True, null=True)
    tag = models.TextField(verbose_name="标签", blank=True, null=True)

    def __str__(self):
        return f"{self.trip_information.trip_name} - 第{self.days}天 - {self.trip_description}"

    class Meta:
        verbose_name = "行程内容"
        verbose_name_plural = "行程内容"
        ordering = ["days", "trip_order"]
