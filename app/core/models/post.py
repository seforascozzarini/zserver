import random
import string

from django.conf import settings
from django.db.models import Q
from django.contrib.gis.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.measure import Distance



def generate_random_digit_string(length):
    """Generate random digit string of specified length."""
    return ''.join(random.choice(string.digits) for _ in range(length))


def generate_unique_post_code(post_type, code_length=7):
    prefix = 'L' if post_type == PostType.LOST else 'F'
    code = prefix + generate_random_digit_string(code_length - len(prefix))
    while Post.objects.filter(code=code).exists():
        code = prefix + generate_random_digit_string(code_length - len(prefix))
    return code

class SearchRadius(models.IntegerChoices):
    VERY_CLOSE = 2000, _('search_radius_very_close')
    CLOSE = 5000, _('search_radius_close')
    NEAR = 10000, _('search_radius_near')
    MODERATE = 15000, _('search_radius_moderate')
    FAR= 20000, _('search_radius_far')
    DISTANT= 30000, _('search_radius_distant')


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
    location = models.PointField(geography=True, srid=4326)
    address = models.CharField(max_length=500)
    pet_type = models.SmallIntegerField(choices=PetType.choices)
    gender = models.SmallIntegerField(
        choices=PetGender.choices,
        default=PetGender.NOT_SPECIFIED
    )
    age_min = models.SmallIntegerField(blank=True, null=True)
    age_max = models.SmallIntegerField(blank=True, null=True)
    
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


class PostQuerySet(models.QuerySet):
    def get_published(self):
        return self.filter(status=PostStatus.PUBLISHED)
    
    def get_lost(self):
        return self.filter(type=PostType.LOST)
    
    def get_found(self):
        return self.filter(type=PostType.FOUND)
    
    def filterby_age(self, min_age, max_age):
        return self.filter(age_min__lte=min_age, age_max__gte=max_age)
    
    def filterby_gender(self, gender, exact=True):
        ''' filter by the exact gender or includes NOT_SPECIFIED if exact=False '''
        if exact:
            return self.filter(gender=gender)
        return self.filter(Q(gender=gender)|Q(gender=PetGender.NOT_SPECIFIED))
    
    def filterby_microchiped(self, microchiped, exact=True):
        ''' filter by the exact microchiped or includes NOT_SPECIFIED if exact=False '''
        if exact:
            return self.filter(microchip=microchiped)
        return self.filter(Q(microchip=microchiped)|Q(microchip=PetMicrochip.NOT_SPECIFIED))
    
    def filterby_sterialised(self, sterialised, exact=True):
        ''' filter by the exact sterialised or includes NOT_SPECIFIED if exact=False '''
        if exact:
            return self.filter(sterilised=sterialised)
        return self.filter(Q(sterilised=sterialised)|Q(sterilised=PetSterilised.NOT_SPECIFIED))
    
    def annotate_distance(self, location):
        ''' annotate the distance from the location in meters '''
        return self.annotate(distance=Distance('location', location))
    
    def filterby_radius(self, location, radius):
        ''' filter by the distance from the location and the radius in meters '''
        self.annotate_distance(location)
        return self.filter(distance__lte=radius)
    
    def very_close_to(self, location):
        return self.filterby_radius(location, SearchRadius.VERY_CLOSE)
    
    def close_to(self, location, include_closer=True):
        if include_closer:
            return self.filterby_radius(location, SearchRadius.CLOSE)
        return self.filter(distance__gt=SearchRadius.VERY_CLOSE, distance__lte=SearchRadius.CLOSE)
    
    def near_to(self, location, include_closer=True):
        if include_closer:
            return self.filterby_radius(location, SearchRadius.NEAR)
        return self.filter(distance__gt=SearchRadius.CLOSE, distance__lte=SearchRadius.NEAR)
    
    def moderate_to(self, location, include_closer=True):
        if include_closer:
            return self.filterby_radius(location, SearchRadius.MODERATE)
        return self.filter(distance__gt=SearchRadius.NEAR, distance__lte=SearchRadius.MODERATE)
    
    def far_to(self, location, include_closer=True):
        if include_closer:
            return self.filterby_radius(location, SearchRadius.FAR)
        return self.filter(distance__gt=SearchRadius.MODERATE, distance__lte=SearchRadius.FAR)
    
    def distant_to(self, location, include_closer=True):
        if include_closer:
            return self.filterby_radius(location, SearchRadius.DISTANT)
        return self.filter(distance__gt=SearchRadius.FAR, distance__lte=SearchRadius.DISTANT)
    
    def search(self, text):
        return self.filter(
            Q(specific_marks__icontains=text)
            | Q(pet_name__icontains=text)
            | Q(text__icontains=text)
            | Q(contacts__icontains=text)
        )
        
    def filterby_user_location(self, user):
        ''' filter by the user location and radius '''
        if user.location is None:
            return self
        return self.filterby_radius(user.location, user.radius)

class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)
    
    def get_related(self, post):
        '''  get probable matches for the post '''
        qs = self.get_queryset().filter(
            ~Q(id=post.id) # exclude the same post
            & ~Q(type=post.type) # exclude the same type
            & Q(pet_type=post.pet_type) # same pet type
            ).published()
        
        # if it is a lost post, consider only the pets found after the lost date
        if post.type == PostType.LOST:
            qs = qs.filter(event_date__gte=post.event_date)

        if post.min_age and post.max_age:
            qs = qs.filterby_age(post.min_age, post.max_age)
        
        qs = qs.filterby_microchiped(post.microchip, exact=False)
        qs = qs.filterby_gender(post.gender, exact=False)
        qs = qs.filterby_sterialised(post.sterialised, exact=False)
        
        # exclude all the posts that are too far
        qs = qs.distant_to(post.location, include_closer=True)
        
        qs = qs.order_by('-gender', '-sterilized', '-microchip', 'distance')
        return qs
        