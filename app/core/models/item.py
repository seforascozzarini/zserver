from django.contrib.gis.db import models
from django.utils import timezone


class Item(models.Model):
    name = models.TextField()
    price = models.FloatField()
    image = models.ImageField()
    type = models.SmallIntegerField()
    create_date = models.DateTimeField(default=timezone.now, editable=False)
    write_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name