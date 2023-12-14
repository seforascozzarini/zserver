from django.db import models
from django.utils import timezone


def story_image_directory_path(instance, filename):
    return f'stories/story_images/%Y/%m/{filename}'


class Story(models.Model):
    text = models.TextField()
    username = models.TextField(default='Anonimo', editable=True)
    is_username_visible = models.BooleanField(default=True, editable=True)
    start_date = models.DateTimeField(default=timezone.now, editable=True)
    end_date = models.DateTimeField(default=timezone.now, editable=True)
    image = models.ImageField(upload_to=story_image_directory_path, verbose_name='Immagine della storia', blank=True)
    create_date = models.DateTimeField(default=timezone.now, editable=False)
    write_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Stories'

    def __str__(self):
        return self.text
