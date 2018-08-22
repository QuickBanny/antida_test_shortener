import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic
from .models import Link
from django.conf import settings
# Create your views here.

class Registry(generic.CreateView):
	form_class = UserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'registration/registry.html'


def index(request):
	if request.user.is_authenticated:
		urls = request.user.link_set.all().order_by('-date_of_creations')
		return render(request, 'url_shortener/home.html', {'urls': urls})
	return render(request, 'url_shortener/home.html')

def redirect_origin_url(request, short_id):
	url = get_object_or_404(Link, short_id=short_id)
	url.count += 1
	url.save()
	return HttpResponseRedirect(url.full_link)

def shorten_url(request):
	if request.user.is_authenticated:
		query = request.GET.get('link')
		user = request.user
		if query != '':
			try:
				url = Link.objects.get(full_link=query, user=user)
				short_link = url.short_link
				return render(request, 'url_shortener/link.html', {'link': short_link})
			except (Link.DoesNotExist):
				short_id = get_short_code()
				short_link = settings.SITE_URL + "/" + short_id
				l = Link(full_link=query, short_id=short_id, 
						short_link=short_link, user=user)
				l.save()
				return render(request, 'url_shortener/link.html', {'link': short_link})
		return redirect('index')
	return redirect('index')


def get_short_code():
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    while True:
        short_id = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Link.objects.get(short_id=short_id)
            return temp
        except:
            return short_id