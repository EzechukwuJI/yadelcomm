from django.shortcuts import render,redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse
# import timezone

from yadel_main.models import UserAccount, MediaCategory, MediaNames, Publication, MediaContact
from yadel_main.forms import EditandPublishForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db.models import F
from django.contrib import messages

from yadel_main.helpers import paginate_list, publish_article
from yadelcommunications.settings import DOMAIN_NAME
import datetime
# Create your views here.



def  indexView(request):
    return HttpResponse('This admin page worked')



@login_required()
def adminDashboardView(request):
	context = {}
	# print "caught admin view......."
	submissions = paginate_list(request, Publication.objects.filter(deleted = False).order_by('status'), 15)
	context['submissions'] = submissions
	return render(request, 'yadel/admin/admin-dashboard.html', context)





@login_required()
def adminUserManager(request):
	return render(request, 'yadel/admin/user-manager.html', {})



@login_required()
def publishArticle(request, **kwargs):
	action    =     kwargs['action']
	if request.user.is_superuser or request.user.is_staff:
		article =  get_object_or_404(Publication, pk = kwargs['pk'])
		selected_media = article.media.strip('[]').encode('utf-8').split(',')
		media_list = [val[2:].replace("'","") for val in selected_media]
		email = article.posted_by.email
		media_contacts_dict = {}
		for media in media_list:
			media = MediaNames.objects.get(media_name = media)
			media_contacts = [contact.person + "-" + contact.contact_email for contact in MediaContact.objects.filter(media = media)]
			media_contacts_dict[media] = media_contacts
		# print media_list
		if request.method == "POST":
			publish_article(request, request.POST['post_action'], article)
			return redirect(reverse('yadel_admin:admin-dashboard'))
		else:
			return render(request, 'yadel/admin/edit-publish.html', {'post':article, 'action':action, 'contact_dict': media_contacts_dict})

	# return render(request, 'yadel/admin/edit-publish.html', {'post':article, 'action':action, 'contact_dict': media_contacts_dict})

			# action   =   rp['post_action']  
			# article_title = ""
			# rp = request.POST
			# if action == "send-to-media":
			# 	media_contact_emails = [val.split('-')[1].encode('utf-8') for val in rp.getlist('media_contact')]
			# 	print "selected media contact ", media_contact_emails
			# 	if rp['new_post_title'] != "":
			# 		article.title 	= 	rp['new_post_title'] # overwrite existing title
			# 		article_title   =   rp['new_post_title']
			# 	else:
			# 		article_title = article.title
			# 	article.content 	= 	rp['post-content']
			# 	article.status 		= 	"processing"
			# 	article_heading 	=  "<div style='padding:5px;text-align:left'><span style='font-size:16px;'>TITLE: &nbsp; " + article_title.upper() + "</span></div>"
			# 	category 			=  "<div style='padding:5px;text-align:left'><strong>Press Material: </strong>" + rp['press_material'] + "<br/></div><br/>"
			# 	text_body           =  "<div style='text-align:justify'>" + rp['post-content'] + "</div>"
			# 	# send post to media jounalists emails
			# 	subject                  =      'Publication submission from Yadel communications'
   #              content                  =       article_heading + category + text_body
   #              sender                   =      'editor@yadelcommunications.com'
   #              recipient_list           =       media_contact_emails
   #              headers  				 =       {}
   #              # try:
   #              article_mail  = EmailMessage(subject = subject, body = content,from_email = sender, bcc = recipient_list)
   #              article_mail.content_subtype = "html" # leaves main type as text/html

   #              if article.pictures:
   #                  attach_image 	= 	article.pictures
   #                  article_mail.attach(attach_image.name, attach_image.read())
   #              else:
   #                  print "No picture to attach..."
   #              article_mail.send(fail_silently = False)
   #              article.save()
   #              return redirect(reverse('yadel_admin:admin-dashboard'))



   #          elif action == "update": 
   #          	print "yes"
        


	# return redirect(reverse('yadel_admin:admin-dashboard'))

	# get return external url
			# link = DOMAIN_NAME + "news/" + str(article.pk) + "/" + article.title_slug

			# # SEND MAIL WITH PASSWORD using sendmail
			# message  = "Hello " + article.posted_by.first_name + ", "
			# message += "Your article has been published on our portal. Use the links below to <br/><br/> " + link
			# message += "start posting your projects. <br/><br/> You are required to change this password once you're logged in.<br/>"

			# message += "Use the link below to change your password.<br/>"
			# message += "<br/><strong> Your logging details are: </strong> <br/><br/> Username: " + email + "<br/>password: " + str(password) + "<br/><br/>"
			# message += "Change your password  <a href=" + link + ">Here </a><br/> <br/> Regards: <br/> The ndoozi.com Team"
			# print message
			# # send email to customer
			# notify  = EmailMessage(subject= 'Your article has been published', body = message, to =[email])
			# notify.content_subtype = 'html'
			# notify.send()











