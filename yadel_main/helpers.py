import random
from yadel_main.models import *
from yadel_main import models
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger



def get_reg_code(useremail):
    code_list = []
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for counter in range(10):
        code_list.append(random.choice(alpha.lower()))
        code_list.append(random.choice(alpha))
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









