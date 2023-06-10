from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class YourModel(models.Model):
    field1 = models.CharField(max_length=100)
    field2 = models.IntegerField()
    # 他のフィールドの定義

    def __str__(self):
        return self.field1

class Users(AbstractUser):
    nickname = models.CharField(max_length=255)
    bank_account = models.CharField(max_length=100)
    profile_picture = models.CharField(max_length=255)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'users'