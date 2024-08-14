from django.db import models


class Chunk(models.Model):
    text = models.TextField()
    embedding = models.BinaryField()
    url = models.URLField()
    keywords = models.CharField(max_length=2000)
