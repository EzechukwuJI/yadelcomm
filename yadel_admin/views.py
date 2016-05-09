from django.shortcuts import render,redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse
# import timezone

from yadel_main.models import UserAccount, MediaCategory, MediaNames, Publication, MediaContact
from yadel_main.forms import EditandPublishForm
from yadel_main import models as main_model

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
def adminDashboardView(request, status):
	context = {}
	submissions = paginate_list(request, Publication.objects.filter(deleted = False).order_by('status','-date_posted'), 10)
	context['submissions'] = submissions
	context['status']  =  status
	if request.method == "POST":
		status = request.POST['search-by-status']
		# print "Article status ", status
		context['status']  =  status
		if status == "all":
			submissions = paginate_list(request, Publication.objects.filter(deleted = False).order_by('status','-date_posted'), 10)
			context['submissions'] = submissions
		else:
			submissions = paginate_list(request, Publication.objects.filter(status = status, deleted = False).order_by('-date_posted'), 10)
			context['submissions'] = submissions
		return render(request, 'yadel/admin/admin-dashboard.html', context)
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
			return redirect(reverse('yadel_admin:admin-dashboard', kwargs = {'status': 'new'}))
		else:
			return render(request, 'yadel/admin/edit-publish.html', {'post':article, 'action':action, 'contact_dict': media_contacts_dict})

	


def contentManager(request):
	context = {}
	
	if request.method == "POST":
		rp = request.POST
		model = rp['object_model']
		object_model = getattr(main_model, rp['object_model'])
		if model == "MediaCategory":
			content = object_model.objects.create(media_type = rp['press_material'], date_added = datetime.datetime.now())
		elif model == "MediaNames":
			content = object_model.objects.create(media_name = rp['media_name'], date_added = datetime.datetime.now())
		elif model == "LatestNews":
			content = object_model.objects.create(news_content = rp['latest_news'], date_added = datetime.datetime.now())
		elif model == "MediaContact":
			media = MediaNames.objects.get(pk = rp['media_house'])
			content = object_model.objects.create(media=media, person = rp['media_contact'],contact_email = rp['media_contact_email'], date_added = datetime.datetime.now())
		if content:
			messages.info(request, "Content successfully created.")
		# print "object model ", object_model
	context['media_category']    =       MediaCategory.objects.all()
	context['media_names']       =       MediaNames.objects.all()
	context['media_contacts']    =  	 MediaContact.objects.all()
	context['clients']           =       UserAccount.objects.filter(user__is_staff = False, user__is_active = True)
	context['members_of_staff']  =       UserAccount.objects.filter(user__is_staff = True, user__is_active = True)
	return render(request, 'yadel/admin/content-manager.html', context)






def delete_content(request, pk, model):
	object_model = getattr(main_model, model)
	content_to_delete = object_model.objects.get(pk = pk)
	content_to_delete.delete()
	messages.info(request, "Item has been deleted")
	return redirect(request.META['HTTP_REFERER'])







