from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
# Create your models here.
from django.contrib.auth.models import User

class Categories(models.Model):
    icon = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    def get_all_categories(self):
        return Categories.objects.all().order_by('id')
    

class Author(models.Model):
    author_profile = models.ImageField(upload_to='Media/featured_img', null=True)
    name = models.CharField(max_length=200, null=True)
    about_author = models.TextField()

    def __str__(self):
        return self.name
    
class Level(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class Language(models.Model):
    language = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.language


class Course(models.Model):
    STATUS = (('PUBLISH','PUBLISH'),('DRAFT', 'DRAFT'))

    featured_image = models.ImageField(upload_to='Media/featured_img', null=True)
    featured_video = models.CharField(max_length=200, null= True)
    title = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    price = models.IntegerField(null=True, default=0)
    discount = models.IntegerField(null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    deadline = models.CharField(max_length=100, null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=100,null=True)
    certificate = models.CharField(max_length=100,null=True)


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("course_details", kwargs={'slug': self.slug})

    

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Course)


class What_You_Learn(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.points
    

class Requirements(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.points
    

class Lession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.name
    
class Video(models.Model):
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to="Media/Yt_Thumbnail", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lession = models.ForeignKey(Lession, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    youtube_id = models.CharField(max_length=100)
    time_duration = models.FloatField(null=True)
    preview = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    paid = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.first_name + " - " + self.course.title



class Payment(models.Model):

    order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    user_course = models.ForeignKey(UserCourse, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)




    def __str__(self) -> str:
        return self.user.first_name + " - " + self.course.title
