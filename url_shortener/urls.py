from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('registry/', views.Registry.as_view(), name='registry'),
	path('shorten_url/', views.shorten_url, name='shorten_url'),
	path('<short_id>/', views.redirect_origin_url, name='redirect_origin_url')   
]
