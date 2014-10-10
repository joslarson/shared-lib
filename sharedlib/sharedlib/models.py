from django.db import models


class album(models.Model):
    name = models.CharField(max_length=255)
    cost = models.IntegerField()
    file_url = models.TextField()
    image_url = models.TextField()
