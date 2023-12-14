from django.db import models
from django.utils import timezone


class Comment(models.Model):
    post = models.ForeignKey('core.Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    upvote = models.SmallIntegerField(blank=True, null=True)
    downvote = models.SmallIntegerField(blank=True, null=True)
    create_date = models.DateTimeField(default=timezone.now, editable=False)
    write_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment for {self.post}'
