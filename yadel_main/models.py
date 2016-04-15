from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User 




PUB_STATUS = (
  ('New',  'New'),
  ('Published',  'published'),
  ('Pending', 'pending'),
  ('Rejected', 'rejected'),
              )




# SALUTATION = (('Mr', 'Mr'),('Mrs','Mrs'),('Dr', 'Dr'),)


class MediaNames(models.Model):
  media_name          =         models.CharField(max_length = 200)
  date_added          =         models.DateTimeField(auto_now_add = True)

  def __unicode(self):
    return '%s' %(self.media_name)


# class PressMaterial(models.Model):
#   media_type                        =         models.CharField(max_length = 150)
#   date_added                        =         models.DateTimeField(auto_now_add = True)

#   def __unicode(self):
#     return '%s' %(self.media_type)



class MediaCategory(models.Model):
  media_type                        =         models.CharField(max_length = 150)
  date_added                        =         models.DateTimeField(auto_now_add = True)

  def __unicode(self):
    return '%s' %(self.media_type)





class UserAccount(models.Model):
    title                            =         models.CharField(max_length = 15)
    user                             =         models.OneToOneField(User)
    phone_no                         =         models.CharField(max_length = 15)
    organization                     =         models.CharField(max_length  =  100, null = True, blank = True)
    date_created                     =         models.DateTimeField(auto_now_add = True)
    is_confirmed                     =         models.BooleanField(default = False)
    registration_code                =         models.CharField(max_length = 25)


    def __unicode__(self):
        return '%s '  %(self.user)



class Publication(models.Model):
    posted_by                       =              models.ForeignKey(User)
    title                           =              models.CharField(max_length = 175)
    title_slug                      =              models.CharField(max_length = 200)
    status                          =              models.CharField(max_length = 25, choices = PUB_STATUS)
    date_posted                     =              models.DateTimeField(auto_now_add = True)
    # press_material                  =              models.ForeignKey(MediaCategory)
    # media                           =              models.ForeignKey(MediaNames)
    press_material                  =              models.CharField(max_length = 125)
    media                           =              models.CharField(max_length = 125)
    content                         =              models.CharField(max_length = 3000)
    pictures                        =              models.FileField(upload_to ='media/')
    document                        =              models.FileField(upload_to ='publication/%Y-%M-%D', null=True, blank = True)
    deleted                         =              models.BooleanField(default = False)
    publish_online                  =              models.BooleanField("Do you also want online publication of the chosen media? ", default = False)


    def save(self, *args, **kwargs):
        self.title_slug  = slugify(self.title)
        super(Publication, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' %(self.title)
    































    
