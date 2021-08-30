from django.db import models


class Information(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=300)
