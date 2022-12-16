from django.db import models
from apps import order

__all__ = [
    'Category',
    'Beat',
    'Ipaddress'
]

class BeatManager(models.Manager):
    def published(self,order='time'):
        return self.filter(is_show=True)

    def free(self,order='time'):
        return self.filter(is_show=True,price=0)

class Ipaddress(models.Model):
    ip_addr = models.GenericIPAddressField()

class Category(models.Model):
    name = models.CharField(max_length=16)
    slug = models.SlugField()
    on_home = models.BooleanField(default=False)

    def __str__(self):
        return self.name
class Beat(models.Model):
    TYPE_CHOICE = [
        ('D','demo'),
        ('F','full'),
    ]

    code = models.PositiveIntegerField(unique=True,blank=True)
    title = models.CharField(max_length=32,unique=True)
    audio_beat = models.FileField(upload_to='public/')
    main_beat = models.FileField(upload_to='prive/',blank=True,null=True)
    time_audio = models.IntegerField(blank=True,null=True)
    image_beat = models.ImageField(upload_to='img/')
    type = models.CharField(max_length=1,choices=TYPE_CHOICE)
    price = models.PositiveIntegerField()
    is_show = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False)
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING,null=True,related_name='beats')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    hits = models.ManyToManyField(Ipaddress,through="BeatHits",blank=True,related_name='hits')

    objects = BeatManager()

    def is_in_order(self):
        return order.models.Order.objects.filter(beat=self).exists()

    def __str__(self):
        return self.title
    
    def get_type(self):
        if self.type == 'D':
            return 'Demo'
        if self.type == 'F':
            return 'Full'
    
    def get_time_humanize(self):
        time = self.time_audio
        minute = time // 60
        secound = time % 60
        return F"{minute}:{secound}"

        

class BeatHits(models.Model):
    beat = models.ForeignKey(Beat,on_delete=models.CASCADE)
    ip_address = models.ForeignKey(Ipaddress,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)