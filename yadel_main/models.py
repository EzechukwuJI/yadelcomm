from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User 

# Create your models here.

PUB_STATUS = (('Published',  'published'),
                              ( 'Pending', 'pending'),
                              ('Rejected', 'rejected'),
              )

CATEGORIES = (('news','news'),
                              ('socials', 'socials'),
                              ('promo','promo'),
                              ('alert', 'alert'),
                              ('others', 'others'),
              )

class UserAccount(models.Model):
    user                             =         models.OneToOneField(User)
    phone_no                    =         models.CharField(max_length = 15)
    organization              =         models.CharField(max_length  =  100)
    date_created              =         models.DateTimeField(auto_now_add = True)


    def __unicode__(self):
        return '%s     %s'  %(self.username, self.organization)


class Publication(models.Model):
    title                           =              models.CharField(max_length = 175)
    title_slug                  =              models.CharField(max_length = 200)
    status                        =              models.CharField(max_length = 25, choices = PUB_STATUS)
    date_posted             =              models.DateTimeField(auto_now_add = True)
    category                   =              models.CharField(max_length = 50, choices = CATEGORIES)
    posted_by                =              models.ForeignKey(User)
    content                     =              models.CharField(max_length = 1500)
    pictures                    =              models.FileField(upload_to ='/media/')
    deleted                     =               models.BooleanField(default = False)


    def save(self, *args, **kwargs):
        self.title_slug  = slugify(self.title)
        super(Publication, self).save(*args, **kwargs)


    def __unicode__(self):
        return '%s' %(self.title)
    
    
