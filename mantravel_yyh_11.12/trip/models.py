from django.db import models

# Create your models here.
class destination(models.Model):
    destination_id = models.AutoField(primary_key=True)  # 自动生成主键ID
    name = models.CharField(max_length=255)             # 存储旅游地址
    description = models.TextField()                    # 存储特色
    tag = models.TextField()

    class Meta:
        db_table = 'destination'  # 指定数据库表名为 'destination'

    def __str__(self):
        return self.name

class TripInformation(models.Model):
    trip_name = models.CharField(max_length=255)
    user_id = models.IntegerField()
    days = models.IntegerField()
    start_date = models.DateField()
    user_token = models.CharField(max_length=255)

    class Meta:
        db_table = 'trip_information'  # 指定数据库中的表名