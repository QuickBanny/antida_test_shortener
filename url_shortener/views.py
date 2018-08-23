import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, View
from url_shortener.models import Link
from django.conf import settings
# Create your views here.

class Registry(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registry.html'

class LinkListView(ListView):
    model = Link
    template_name = 'url_shortener/links.html'

    def get_queryset(self):
        return Link.objects.all().filter(user=self.request.user).order_by('-date_of_creations')

class CreateShortViews(CreateView):
    model = Link

    def get(self, request):
        query = request.GET.get('link')
        user = request.user
        if query != '':
            try:
                url = Link.objects.get(full_link=query, user=user)
                res = url.short_link
            except (Link.DoesNotExist):
                short_id = get_short_code()
                res = settings.SITE_URL + "/" + short_id
                l = Link(full_link=query, short_id=short_id, 
                        short_link=res, user=user)
                l.save()
            return render(request, 'url_shortener/link.html', {'link': res})
        return redirect('link-list')

class HomeViews(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('link-list')
        return render(request, 'url_shortener/home.html')

def redirect_origin_url(request, short_id):
    url = get_object_or_404(Link, short_id=short_id)
    url.count += 1
    url.save()
    return HttpResponseRedirect(url.full_link)

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