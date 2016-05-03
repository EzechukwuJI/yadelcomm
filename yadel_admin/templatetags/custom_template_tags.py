from django import template
# from django.template.defaultfilters import stringfilter
from django.shortcuts import get_object_or_404
from yadel_main.models import Publication


register = template.Library()


@register.filter(name = 'get_post_media')
def get_post_media(post_id):
	media_list = []
	post = get_object_or_404(Publication, pk = post_id)
	post_media = post.media.strip('[]').encode('utf-8').split(',')
	media_list = [val[2:].replace("'","") for val in post_media]
	return media_list