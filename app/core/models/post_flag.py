from django.contrib.gis.db import models
from django.utils import timezone


class PostFlag(models.Model):
    """Post flag model."""
    post = models.ForeignKey('core.Post', on_delete=models.CASCADE, related_name='post_flags')
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return str(self.pk)
