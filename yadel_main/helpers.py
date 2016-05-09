import random, datetime
from yadel_main.models import *
from yadel_main import models
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.shortcuts import render,redirect, get_object_or_404
from django.core.urlresolvers import reverse
from yadelcommunications.settings import DOMAIN_NAME, DEFAULT_FROM_EMAIL



def get_reg_code(useremail):
    code_list = []
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for counter in range(10):
        code_list.append(random.choice(alpha.lower()))
        code_list.append(random.choice(alpha[::-1]))
        code_list.append(random.choice(useremail.split('@')[0]))
    return "".join(code_list)




def get_content_tuple(objectmodel, **kwargs):
    content_tuple = ()
    if objectmodel == MediaCategory:
        for item in objectmodel.objects.all():
            item_tuple = ((item.media_type, item.media_type),) 
            content_tuple += item_tuple
    elif objectmodel == MediaNames:
    	for item in objectmodel.objects.all():
            item_tuple = ((item.media_name, item.media_name),) 
            content_tuple += item_tuple
    # print "content_tuple", content_tuple
    return content_tuple



def paginate_list(request, objects_list, num_per_page):
    paginator   =   Paginator(objects_list, num_per_page) # show number of jobs per page
    page  = request.GET.get('page')
    try:
        paginated_list  = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        paginated_list   =   paginator.page(1)
    except  EmptyPage:
        #if page is out of range(e.g 9999), deliver last page of results
        paginated_list      =   paginator.page(paginator.num_pages)
    return paginated_list




def publish_article(request, action, article):
    # action   =   rp['post_action']  
    article_title = ""
    rp = request.POST
    if action == "send-to-media":
        print "preparing to send to media..."
        media_contact_emails = [val.split('-')[1].encode('utf-8') for val in rp.getlist('media_contact')]
        print "selected media contact ", media_contact_emails
        if rp['new_post_title'] != "":
            article.title   =   rp['new_post_title'] # overwrite existing title
            article_title   =   rp['new_post_title']
        else:
            article_title = article.title
        article.content     =   rp['post-content']
        article.status      =   "processing"
        article_heading     =  "<div style='padding:5px;text-align:left'><span style='font-size:16px;'>TITLE: &nbsp; " + article_title.upper() + "</span></div>"
        category            =  "<div style='padding:5px;text-align:left'><strong>Press Material: </strong>" + rp['press_material'] + "<br/></div><br/>"
        text_body           =  "<div style='text-align:justify'>" + rp['post-content'] + "</div>"
        # send post to media jounalists emails
        subject                  =      'Publication submission from Yadel communications'
        content                  =       article_heading + category + text_body
        sender                   =      'editor@yadelcommunications.com'
        recipient_list           =       media_contact_emails
        headers                  =       {}
        # try:
        article_mail  = EmailMessage(subject = subject, body = content,from_email = sender, bcc = recipient_list)
        article_mail.content_subtype = "html" # leaves main type as text/html

        if article.pictures:
            attach_image    =   article.pictures
            article_mail.attach(attach_image.name, attach_image.read())
        else:
            print "No picture to attach..."
        # article_mail.send(fail_silently = False)
        article.save()
        # return redirect(reverse('yadel_admin:admin-dashboard'))
    elif action == "update":
        clients_email = article.posted_by.email
        url_list  =  rp.getlist('post_url[]')
        article.redirect_url = url_list
        article.status = "published"
        article.date_published = datetime.datetime.now()
        article.published_by = request.user

        # send notification to client
        internal_post_link = DOMAIN_NAME + "news/" + str(article.pk) + "/" + article.title_slug
        message  = "Hello " + article.posted_by.first_name 
        message += "<br/><br/> We are happy to inform you that your article has been published on the media platform(s) you selected."
        message += "<br/> The links to the publication are listed below. <br/><br/>" 
        for link in url_list:
            message += link + "<br/>"
        message += "You can also view these links by logging into your account on &nbsp; " + DOMAIN_NAME
        message += "<br/> or by clicking the link below. &nbsp; <br/><br/>" + internal_post_link

        subject                  =      "[Yadelcommunications] Your article has been published."
        content                  =       message
        sender                   =       DEFAULT_FROM_EMAIL
        recipient_list           =       clients_email
        headers                  =       {}
        # try:
        article_mail  = EmailMessage(subject = subject, body = content,from_email = sender, to = [recipient_list])
        article_mail.content_subtype = "html" # leaves main type as text/html
        if article.pictures:
            attach_image    =   article.pictures
            article_mail.attach(attach_image.name, attach_image.read())
        else:
            print "No picture to attach..."
        # article_mail.send(fail_silently = False)
        article.save()
        # return redirect(reverse('yadel_admin:admin-dashboard'))
        
















































