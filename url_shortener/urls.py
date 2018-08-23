from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
	path('', views.HomeViews.as_view(), name='home'),
	path('links/', views.LinkListView.as_view(), name='link-list'),
	path('registry/', views.Registry.as_view(), name='registry'),
	path('short/', login_required(views.CreateShortViews.as_view()), name='short'),
	path('<short_id>/', views.redirect_origin_url, name='redirect_origin_url')   
]
