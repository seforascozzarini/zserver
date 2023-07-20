from django.contrib.gis.db import models

from django.utils import timezone


class Advice(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now, editable=False)
    write_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
