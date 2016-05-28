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


@register.filter(name = 'get_post_url')
def get_post_url(post_id):
	post = Publication.objects.get(id = post_id)
	url =  post.redirect_url.strip('[]').encode('utf-8').split(',')[0][2:].replace("'","")
	if url.startswith("www"):
		url = "http://" + url
	return url


@register.filter(name = 'get_all_post_url')
def get_all_post_url(post_id):
	cleaned_url = []
	# post = Publication.objects.get(id = post_id)
	post = get_object_or_404(Publication, id = post_id)
	url_list =  post.redirect_url.strip('[]').encode('utf-8').split(',')
	print len(url_list)
	for url in url_list:

		if url.startswith("www"):
			url = "http://" + url
		cleaned_url.append(url)
	return cleaned_url
