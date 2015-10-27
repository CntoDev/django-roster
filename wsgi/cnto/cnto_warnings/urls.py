"""cnto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import cnto_warnings.views as warning_views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^list/$', warning_views.list_warnings, name='list-warnings'),
    url(r'^list-for-member/(?P<member_pk>\d+)/$', warning_views.list_warnings_for_member,
        name='list-warnings-for-member'),
    url(r'^toggle-warning-acknowledge/(?P<pk>\d+)/$', warning_views.toggle_member_acknowledge,
        name='toggle-warning-acknowledge'),
]
