from django import forms
from django.contrib.auth.models import User

from yadel_main.models import *

from yadel_main.helpers import get_content_tuple

from multiupload.fields import MultiFileField

# class UploadForm(forms.Form):
#     attachments = MultiFileField(min_num=1, max_num=3, max_file_size=1024*1024*5)


class LoginForm(forms.ModelForm):
	email = forms.EmailField(max_length = 128, help_text = "",widget=forms.TextInput
		(attrs={'class':'form-control','placeholder': 'Email','autofocus':'autofocus','required':'required'}))

	password = forms.CharField(max_length=10,required=True, widget=forms.PasswordInput
		(attrs={'class' : 'form-control','placeholder':'Password','required':'required'}))
	
	class Meta:
		# Associate form with a model
		model = User
		fields = ('email','password',)



# class UserAccountForm(forms.ModelForm):
# 	email = forms.EmailField(max_length = 128, help_text = "",widget=forms.TextInput
# 		(attrs={'class':'form-control','placeholder': 'Email','autofocus':'autofocus','required':'required'}))

# 	password = forms.CharField(max_length=10,required=True, widget=forms.PasswordInput
# 		(attrs={'class' : 'form-control','placeholder':'Password','required':'required'}))
	
# 	class Meta:
# 		# Associate form with a model
# 		model = User
# 		fields = ('email','password',)




SALUTATION = (('Mr', 'Mr'),('Mrs','Mrs'),('Dr', 'Dr'),)
class UserAccountForm(forms.ModelForm):
	title           =    forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control', 'required':True}), choices = SALUTATION)
	username        =    forms.CharField(max_length = 128, help_text = "",widget=forms.TextInput(attrs={'class' : 'form-control','placeholder': 'Username', 'required':'required','autofocus':'autofocus'}))
	email           =    forms.EmailField(max_length = 128, help_text = "",widget=forms.EmailInput(attrs={'class' : 'form-control', 'placeholder': 'Email','required':'required'}))
	password        =    forms.CharField(max_length=15, widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder':'Password','required':'required'}))
	first_name      =    forms.CharField(max_length = 128, help_text = "",widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'First Name', 'required':'required'}))
	last_name       =    forms.CharField(max_length = 128, help_text = "",widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Last Name', 'required':'required'}))

	class Meta:
		model = User
		fields =  ('title', 'username','email','password','first_name','last_name')




# MEDIA_CATEGORY     =       yadel_main.helpers.
# MEDIA_HOUSES       =       yadel_main.helpers.

class PublicationForm(forms.ModelForm):
	

	title              =       forms.CharField(max_length = 125, help_text = "",widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Enter a title for you article','required':'required'}))
	press_material     =       forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control', 'required':True}), choices = get_content_tuple(MediaCategory))
	person_to_quote    =       forms.CharField(max_length = 125, help_text = "",widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Name to be mentioned in publication'}))
	persons_position   =       forms.CharField(max_length = 125, help_text = "",widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': "person's position"}))
	media              =       forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'form-control', 'required':True}), choices = get_content_tuple(MediaNames))
	pictures           =       forms.ImageField(help_text="", widget=forms.FileInput(attrs={'style':'font-size:15px;','multiple':'multiple'}))
	# document           =       forms.FileField(help_text="", widget=forms.FileInput(attrs={'style':'font-size:15px;'}))
	content            =       forms.CharField(max_length = 3000, help_text = "", widget=forms.Textarea
		(attrs={'class':'form-control', 'rows': 10, 'placeholder': 'You can type or  copy and paste your article here. '}))
	# pictures           =       forms.ImageField(help_text="", widget=forms.FileInput(attrs={'class':'form-control', 'id':'proj_pic','style':'font-size:15px;'}))
	


	class Meta:
		model     =     Publication
		fields    =     ('title','press_material', 'media','content', 'pictures', 'publish_online','person_to_quote','persons_position')



class DocumentUploadForm(forms.ModelForm):
	document           =       forms.FileField(help_text="", widget=forms.FileInput(attrs={'style':'font-size:15px;'}))

	class Meta:
		model 		   = 	   PubDocument
		fields 		   = 	   ('document',)





class EditandPublishForm(forms.ModelForm):
	# title              =       forms.CharField(max_length = 125, help_text = "",widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Enter a title for you article','required':'required'}))
	# press_material     =       forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control', 'required':True}), choices = get_content_tuple(MediaCategory))
	# media              =       forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'form-control', 'required':True}), choices = get_content_tuple(MediaNames))
	# pictures           =       forms.ImageField(help_text="", widget=forms.FileInput(attrs={'style':'font-size:15px;'}))
	# document           =       forms.FileField(help_text="", widget=forms.FileInput(attrs={'style':'font-size:15px;'}))
	content            =       forms.CharField(max_length = 3000, help_text = "", widget=forms.Textarea
		(attrs={'class':'form-control', 'required':True, 'rows': 25,'style':'height:auto'}))

	class Meta:
		model = Publication
		fields = ('content','pictures','redirect_url')

























