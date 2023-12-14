import random
import string

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField


def generate_random_digit_string(length):
    """Generate random digit string of specified length."""
    return ''.join(random.choice(string.digits) for _ in range(length))


def generate_unique_post_code(post_type, code_length=7):
    prefix = 'L' if post_type == PostType.LOST else 'F'
    code = prefix + generate_random_digit_string(code_length - len(prefix))
    while Post.objects.filter(code=code).exists():
        code = prefix + generate_random_digit_string(code_length - len(prefix))
    return code


class PostType(models.IntegerChoices):
    LOST = 1, _('post_type_lost')
    FOUND = 2, _('post_type_found')


class PostStatus(models.IntegerChoices):
    DRAFT = 0, _('post_status_draft')
    PUBLISHED = 1, _('post_status_published')
    CLOSED = 2, _('post_status_closed')


class PetType(models.IntegerChoices):
    CAT = 1, _('pet_cat')
    DOG = 2, _('pet_dog')
    BIRD = 3, _('pet_bird')
    RABBIT = 4, _('pet_rabbit')
    TURTLE = 5, _('pet_turtle')
    REPTILE = 6, _('pet_reptile')
    HAMSTER = 7, _('pet_hamster')
    FERRET = 8, _('pet_ferret')
    OTHER = 99, _('pet_other')


class PetGender(models.IntegerChoices):
    NOT_SPECIFIED = 0, _('pet_gender_not_specified')
    MALE = 1, _('pet_gender_male')
    FEMALE = 2, _('pet_gender_female')


class PetMicrochip(models.IntegerChoices):
    NOT_SPECIFIED = 0, _('pet_microchip_not_specified')
    YES = 1, _('pet_microchip_yes')
    NO = 2, _('pet_microchip_no')


class PetSterilised(models.IntegerChoices):
    NOT_SPECIFIED = 0, _('pet_sterilised_not_specified')
    YES = 1, _('pet_sterilised_yes')
    NO = 2, _('pet_sterilised_no')


class Post(models.Model):
    """Post model."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    code = models.CharField(max_length=10, editable=False, unique=True)
    type = models.SmallIntegerField(choices=PostType.choices)
    location = ArrayField(default=list, base_field=models.FloatField())
    address = models.CharField(max_length=500)
    pet_type = models.SmallIntegerField(choices=PetType.choices)
    gender = models.SmallIntegerField(
        choices=PetGender.choices,
        default=PetGender.NOT_SPECIFIED
    )
    age = models.SmallIntegerField(blank=True, null=True)
    microchip = models.SmallIntegerField(
        choices=PetMicrochip.choices,
        default=PetMicrochip.NOT_SPECIFIED
    )
    sterilised = models.SmallIntegerField(
        choices=PetSterilised.choices,
        default=PetSterilised.NOT_SPECIFIED
    )
    specific_marks = models.CharField(max_length=500, blank=True)
    pet_name = models.CharField(max_length=100, blank=True)
    text = models.TextField()
    contacts = models.JSONField(blank=True, null=True)
    status = models.SmallIntegerField(
        choices=PostStatus.choices,
        default=PostStatus.DRAFT
    )
    event_date = models.DateTimeField(default=timezone.now, editable=True)
    create_date = models.DateTimeField(default=timezone.now, editable=False)
    write_date = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    close_date = models.DateTimeField(blank=True, null=True)

    @property
    def is_flagged(self):
        return self.post_flags.count() > 0

    @property
    def default_image(self):
        try:
            return self.post_images.get(is_default=True).image.path
        except PostImage.DoesNotExist:
            return None

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.code == '':
            self.code = generate_unique_post_code(self.type)
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.code


def post_image_directory_path(instance, filename):
    return f'posts/user_{instance.post.user.pk}/{filename}'


class PostImage(models.Model):
    post = models.ForeignKey('core.Post', on_delete=models.CASCADE, related_name='post_images')
    is_default = models.BooleanField(default=False)
    image = models.ImageField(upload_to=post_image_directory_path, verbose_name='Immagine del post', blank=True)
    description = models.TextField()
    create_date = models.DateTimeField(default=timezone.now, editable=False)
