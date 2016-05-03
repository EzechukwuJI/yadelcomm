from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User 




PUB_STATUS = (
  ('new',  'new'),
  ('published',  'published'),
  ('processing', 'processing'),
  ('rejected', 'rejected'),
              )




# SALUTATION = (('Mr', 'Mr'),('Mrs','Mrs'),('Dr', 'Dr'),)


class MediaNames(models.Model):
  media_name          =           models.CharField(max_length = 200)
  date_added          =           models.DateTimeField(auto_now_add = True)
  contact_persons     =           models.ManyToManyField(User)


  def __unicode__(self):
    return '%s' %(self.media_name)




class MediaContact(models.Model):
  media               =           models.ForeignKey(MediaNames)
  person              =           models.CharField(max_length = 125)
  date_added          =           models.DateTimeField(auto_now_add = True)
  contact_email       =           models.CharField(max_length = 225)


  def __unicode__(self):
    return '%s %s %s %s %s' %(self.media.media_name,"|", self.person, "|", self.contact_email)



# class PressMaterial(models.Model):
#   media_type                        =         models.CharField(max_length = 150)
#   date_added                        =         models.DateTimeField(auto_now_add = True)

#   def __unicode(self):
#     return '%s' %(self.media_type)



class MediaCategory(models.Model):
  media_type                        =         models.CharField(max_length = 150)
  date_added                        =         models.DateTimeField(auto_now_add = True)


  def __unicode__(self):
    return '%s' %(self.media_type)




# class MediaHouse(models.Model):
#   name                =           models.CharField(max_length = 175)
  


#   def __unicode__(self):
#     return self.name










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
    status                          =              models.CharField(max_length = 25, choices = PUB_STATUS, default = "new")
    date_posted                     =              models.DateTimeField(auto_now_add = True)
    # press_material                =              models.ForeignKey(MediaCategory)
    # media                         =              models.ForeignKey(MediaNames)
    press_material                  =              models.CharField(max_length = 125)
    media                           =              models.CharField(max_length = 125)
    content                         =              models.TextField(max_length = 3000)
    pictures                        =              models.FileField(upload_to ='media/')
    document                        =              models.FileField(upload_to ='publication/%Y-%M-%D', null=True, blank = True)
    deleted                         =              models.BooleanField(default = False)
    publish_online                  =              models.BooleanField("Do you also want online publication of the chosen media? ", default = False)
    published_by                    =              models.ForeignKey(User, related_name="Edited_and_published_by", null = True, blank = True)
    date_published                  =              models.DateTimeField(auto_now_add = False, null=True, blank=True)
    redirect_url                    =              models.URLField(max_length = 200, blank = True, null = True, default= None)

    def save(self, *args, **kwargs):
        self.title_slug  = slugify(self.title)
        # self.media       = ";".join(self.media)
        super(Publication, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' %(self.title)
    































    
