from django.db import models
from django.utils import timezone


class CommentFlag(models.Model):
    post = models.ForeignKey('core.Post', on_delete=models.CASCADE, related_name='comment_flags')
    comment = models.ForeignKey('core.Comment', on_delete=models.CASCADE, related_name='comment_flags')
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f'flag for comment {self.pk}'
