from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db.models import F
from django.contrib import messages

from yadel_main.models import UserAccount, MediaCategory, MediaNames, Publication, ClientFeedback, LatestNews, PubDocument
from yadel_main.forms import LoginForm, UserAccountForm,PublicationForm,DocumentUploadForm
from yadel_main.helpers import get_reg_code, paginate_list
from yadelcommunications.settings import DOMAIN_NAME

# Create your views here.



def  indexView(request):
    context = {}
    try:
        context['latest_news'] = LatestNews.objects.all().order_by('-date_added')[0]
    except(IndexError):
        context = {}
    return render(request, 'yadel/general/index.html', context)


def  aboutUsView(request):
    return render(request, 'yadel/general/about.html', {})


# def  servicesView(request):
#     return render(request, 'yadel/general/services.html', {})



def  newsroomView(request):
    articles = paginate_list(request, Publication.objects.filter(deleted = False, status = "published").order_by('-date_posted'), 5)
    return render(request, 'yadel/general/newsroom.html', {'articles':articles})





def  TandCView(request):
    return render(request, 'yadel/general/tandc.html', {})




def  contactView(request):
    if request.method == "POST":
        rp = request.POST
        feedback = ClientFeedback.objects.create(sender = rp['sender'],email = rp['sender_email'], message = rp['message'])
        if feedback:
            messages.info(request, "Thank you for reaching out to us. We will respond to your request within 48 hours")
            subject = '[Yadelcommunications] - New message from ' + rp['sender']
            notify  = EmailMessage(subject= subject, body = rp['message'], to =['editor@yadelcommunications.com'])
            notify.content_subtype = 'html'
            notify.send()
        else:
            messages.warning(request, "Ooops! Sorry something went wrong while trying to post your message, please try again. If this error persists kindly shoot us a mail.")
    return render(request, 'yadel/general/contact.html', {})










def  signUpView(request):
    form = UserAccountForm()
    context = {}
    username = ""
    context['signup_form']         =  form

    if  request.method            ==     "POST":
        sender                     =     request.POST
        reg_code                   =     get_reg_code(sender['email'])
        user_account_form          =     UserAccountForm(data = request.POST)
        if User.objects.filter(username = sender['username']).exists():
            context['signup_form']  =  UserAccountForm(data = request.POST)
            context['username_is_taken']   = True
            return render(request, 'yadel/general/signup.html', context)
        if User.objects.filter(email = sender['email']).exists():
            context['signup_form']  =  UserAccountForm(data = request.POST)
            context['email_is_taken']   = True
            return render(request, 'yadel/general/signup.html', context)
        else:
            if user_account_form.is_valid:
                user = User.objects.create(username = sender['username'], email = sender['email'].lower(),
                    first_name = sender['first_name'], last_name = sender['last_name'])
                user.set_password(sender['password']) 
                user.save()
                UserAccount.objects.create(user = user, phone_no = sender['phone_no'], registration_code = reg_code, organization=sender['company-name'])
                confirmation_link = DOMAIN_NAME + "/confirm-registration/" + reg_code
                message = "Hello " + sender['first_name'].title() + ",<br/><br/>"
                message += "Thank you for signing up on our portal. Click <a href=" + confirmation_link + "> here </a> to confirm your email address."
                message +=  "<br/> If the link above is not responding, copy the link below into your browser. <br/><br/>" + confirmation_link
                message += "<br/> <br/> Yours in Service. <br/>" + DOMAIN_NAME
                
                notify  = EmailMessage(subject= '[Yadel Communications] Confirm your registration', body = message, to =[sender['email']])
                notify.content_subtype = 'html'
                # notify.send()
                context['user_is_created']  =    True
                context['email']            =    sender['email']
                print "user creation for %s successful" %(user)
                print confirmation_link
                return redirect(reverse('yadel_main:registration_success'))
            else:
                return render(request, 'yadel/general/signup.html', context)
    return render(request, 'yadel/general/signup.html', context)


    
    # return render(request, 'yadel/general/signup.html', context)




def confirmEmail(request,code):
    user_to_confirm = UserAccount.objects.filter(registration_code = code) # try get_object_or_404
    if user_to_confirm.exists():
        user_to_confirm.update(is_confirmed = True)
        messages.success(request, "Thank You!. Your email address has been confirmed. Kindly log in below")
    else:
        pass
    return redirect(reverse('yadel_main:login'))








def  loginView(request):
    form = LoginForm()
    context = {}
    username = ""
    context['loginform']  =  form
    if request.method   ==  'POST':
        loginForm       =    LoginForm(data = request.POST)
        if loginForm.is_valid():
            email           =     request.POST.get('email').strip()
            password        =     request.POST.get('password').strip()
            user_account =  User.objects.filter(email = email)
            if user_account.exists():
                username = user_account[0].username
            auth_user       =     authenticate(username = username, password = password)
            if auth_user is not None:
                user  =  auth_user
                if user.is_active:
                    login(request, user) # log user in
                    # #check login source page
                    if request.POST.get('next')  != "":
                        next  =   request.POST.get('next')
                        return redirect(next) # return to the called page
                    if user.is_staff or user.is_superuser:
                        print "redirecting here."
                        return redirect(reverse('yadel_admin:admin-dashboard', kwargs = {'status':'new'}))
                    else:
                        return redirect(reverse('yadel_main:user-dashboard'))
                else:
                    context['inactive'] = True
                    return render(request,  'yadel/general/signin.html', context)
            else:
                context['not_found']   =  True
                return render(request,  'yadel/general/signin.html', context)
        else:
            context['invalid_form']  = True
            return render(request,  'yadel/general/signin.html', context)
    else:
        return render(request,  'yadel/general/signin.html', context)
    return render(request, 'yadel/general/signin.html', {'form':form})







def loadExternalNews(request, **kwargs):
    article = get_object_or_404(Publication, pk = kwargs['pk'])
    articles = Publication.objects.filter(deleted = False, status = "published")
    return render(request, 'yadel/general/news-detail.html', {'article':article,'articles':articles})



def  logoutView(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('yadel_main:index'))




@login_required()
def dashboardView(request, **kwargs):
    context = {}
    template = ""
    template = 'yadel/general/client-dashboard.html'
    articles = paginate_list(request, Publication.objects.filter(posted_by = request.user, deleted=False, status = "published").order_by('-date_posted'), 5)
    return render(request, template, {'articles':articles})








@login_required()
def createArticleView(request):
    articles = Publication.objects.filter(posted_by = request.user, deleted=False, status = "published").order_by('-date_posted')
    article_form = PublicationForm()
    article_doc_form = DocumentUploadForm()
    media_categories  =  MediaCategory.objects.all()
    media_names = MediaNames.objects.all()
    if request.method == "POST":
        # print "post method"
        rp = request.POST
        # print rp
        # print request.FILES
        form = PublicationForm(request.POST, request.FILES)
        doc_form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid() and doc_form.is_valid():
            article = form.save(commit = False)
            article.posted_by = request.user
            article.status = "new"
            article.save()
            upload_doc = PubDocument(document = request.FILES['document'], publication = article)
            upload_doc.save()
            messages.success(request, "Thank You. Your article has been submitted for publication, We will notify you as soon as this article is published")
        else:
            print form.errors
            return render(request, 'yadel/general/submit-article.html', {'article_form':article_form, 'doc_form':article_doc_form, 'media_names':media_names, 'media_categories':media_categories,'articles':articles})
    return render(request, 'yadel/general/submit-article.html', {'article_form':article_form,'doc_form':article_doc_form, 'media_names':media_names, 'media_categories':media_categories, 'articles':articles})







# def clientFeedback(request):












