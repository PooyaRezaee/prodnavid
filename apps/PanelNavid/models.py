from django.db import models
from django.core.cache import cache
from apps.accounts.models import User
from django.conf import settings
from translated_fields import TranslatedField
from django.utils.translation import gettext as _

class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)
    
    def set_cache(self):
        cache.set(self.__class__.__name__, self)

def get_root():
    if settings.DEBUG:
        root = 'static'
    else:
        root = str(settings.STATIC_ROOT)

    return root

class SiteSettings(SingletonModel):
    email = models.EmailField(default='navid.g.h.909xx@gmail.com')
    adress = models.CharField(max_length=256,default='',blank=True)
    phonenumber = models.CharField(max_length=13, default='',blank=True)
    instagram = models.CharField(max_length=256, default='prodnavid',blank=True)
    linkedin = models.CharField(max_length=256, default='',blank=True)
    about = TranslatedField(models.CharField(max_length=1024,default='I am Navid And Create Beat'))
    background = models.ImageField(upload_to='background/',blank=True,null=True)
    stop_seling = models.BooleanField(default=False)
    cdn_active = models.BooleanField(default=False)

class Message(models.Model):
    subject = models.CharField(max_length=30,verbose_name=_('Subject'))
    message = models.CharField(max_length=256,verbose_name=_('Message'))
    meta = models.CharField(max_length=128,blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    created = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

class InfoDeveloper(SingletonModel):
    email = models.EmailField(default='pooya.rezaee.official@gmail.com')
    phonenumber = models.CharField(max_length=13, default='+989396231180',blank=True)
    instagram = models.CharField(max_length=256, default='',blank=True)
    github = models.CharField(max_length=256, default='https://github.com/pooyarezaee',blank=True)
    linkedin = models.CharField(max_length=256, default='https://linkedin.com/in/pooya-rezeemoghadam',blank=True)
    about = TranslatedField(models.CharField(max_length=1024,default='I am PooyaRezaee(Developer This WebApplication'))