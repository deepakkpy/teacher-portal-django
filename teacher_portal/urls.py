
from django.urls import path, include
from portal.views import index_redirect

urlpatterns = [
    path('', index_redirect, name='index'),
    path('', include('portal.urls')),
]
