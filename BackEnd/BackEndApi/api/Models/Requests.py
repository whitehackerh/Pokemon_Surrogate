from django.db import models

class Requests(models.Model):
    client_id = models.IntegerField()
    game_title_id = models.IntegerField()
    category = models.IntegerField()
    request_title = models.CharField(max_length=255)
    description = models.TextField()
    min_price = models.IntegerField()
    max_price = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        app_label = 'api'
        db_table = 'requests'
