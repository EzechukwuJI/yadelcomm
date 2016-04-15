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

from yadel_main.models import UserAccount, MediaCategory, MediaNames, Publication
from yadel_main.forms import LoginForm, UserAccountForm,PublicationForm
from yadel_main.helpers import get_reg_code, paginate_list
from yadelcommunications.settings import DOMAIN_NAME

# Create your views here.



def  indexView(request):
    return render(request, 'yadel/index.html', {})


def  aboutUsView(request):
    return render(request, 'yadel/index.html', {})


def  servicesView(request, service_type):
    return render(request, 'yadel/services.html', {})



def  newsroomView(request):
    articles = paginate_list(request, Publication.objects.all().order_by('-date_posted'), 5)
    return render(request, 'yadel/newsroom.html', {'articles':articles})



def  TandCView(request):
    return render(request, 'yadel/tandc.html', {})

def  contactView(request):
    return render(request, 'yadel/contact.html', {})





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
            return render(request, 'yadel/signup.html', context)
        if User.objects.filter(email = sender['email']).exists():
            context['signup_form']  =  UserAccountForm(data = request.POST)
            context['email_is_taken']   = True
            return render(request, 'yadel/signup.html', context)
        else:
            if user_account_form.is_valid:
                user = User.objects.create(username = sender['username'], email = sender['email'].lower(),
                    first_name = sender['first_name'], last_name = sender['last_name'])
                user.set_password(sender['password']) 
                user.save()
                UserAccount.objects.create(user = user, phone_no = sender['phone_no'], registration_code = reg_code, organization=sender['company-name'])
                confirmation_link = DOMAIN_NAME + "confirm-registration/" + reg_code
                message = "Hello " + sender['first_name'].title() + ",<br/><br/>"
                message += "Thank you for signing up on our portal. Click <a href=' " + confirmation_link + " '> here </a> to confirm your email address."
                message +=  "<br/> If the link above is not responding, copy the link below into your browser. <br/><br/>" + confirmation_link
                message += "<br/> <br/> Yours in Service. <br/>" + DOMAIN_NAME
                
                notify  = EmailMessage(subject= 'Confirm your registration', body = message, to =[sender['email']])
                notify.content_subtype = 'html'
                notify.send()
                context['user_is_created']  =    True
                context['email']            =    sender['email']
                print "user creation for %s successful" %(user)
                return redirect(reverse('yadel_main:registration_success'))
            else:
                return render(request, 'yadel/signup.html', context)
    return render(request, 'yadel/signup.html', context)


    
    # return render(request, 'yadel/signup.html', context)




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
                    if user.is_staff:
                        return redirect(reverse('yadel_admin:admin-dashboard'))
                    else:
                        return redirect(reverse('yadel_main:user-dashboard'))
                else:
                    context['inactive'] = True
                    return render(request,  'yadel/signin.html', context)
            else:
                context['not_found']   =  True
                return render(request,  'yadel/signin.html', context)
        else:
            context['invalid_form']  = True
            return render(request,  'yadel/signin.html', context)
    else:
        return render(request,  'yadel/signin.html', context)
    return render(request, 'yadel/signin.html', {'form':form})







def loadExternalNews(request, **kwargs):
    return render(request, 'yadel/news-detail.html', {'title':kwargs['news_title']})



def  logoutView(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('yadel_main:index'))




@login_required()
def dashboardView(request, **kwargs):
    context = {}
    template = ""
    if not request.user.is_staff or request.user.is_superuser:
        template = 'client/client-dashboard.html'
        articles = paginate_list(request,Publication.objects.filter(posted_by = request.user).order_by('-date_posted'), 5)
    else:
        template = 'admin/admin-dashboard.html'
        paginate_list(request, Publication.objects.all().order_by('-date_posted'), 5)
    return render(request, template, {'articles':articles})








@login_required()
def createArticleView(request):
    article_form = PublicationForm()
    if request.method == "POST":
        rp = request.POST
        form = PublicationForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit = False)
            article.posted_by = request.user
            article.status = "New"
            if article.save():
                messages.success(request, "Thank You. Your article has been submitted for publication on %s , We will notify you as soon as this article is published") %(article.media)
            else:
                messages.error(request, "Opp! Something went wrong. Please try again.")
        else:
            return render(request, 'yadel/submit-article.html', {'article_form':article_form})

    # else:


    return render(request, 'yadel/submit-article.html', {'article_form':article_form})



















