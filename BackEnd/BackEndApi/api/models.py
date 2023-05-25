from django.db import models

class YourModel(models.Model):
    field1 = models.CharField(max_length=100)
    field2 = models.IntegerField()
    # 他のフィールドの定義

    def __str__(self):
        return self.field1
