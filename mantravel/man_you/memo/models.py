from django.db import models

# Create your models here.
class Memo(models.Model):
    title = models.CharField(max_length=100)
    remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('yes', '带了行李'),
        ('no', '没带行李'),
    ]
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='no')
    def __str__(self):
        return self.title