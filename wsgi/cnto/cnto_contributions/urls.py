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
import cnto_contributions.views as contribution_views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^delete/(?P<contribution_pk>\d+)/$', contribution_views.delete_contribution, name='delete-contribution'),
    url(r'^edit/(?P<contribution_pk>\d+)/$', contribution_views.edit_contribution, name='edit-contribution'),
    url(r'^edit-collection/(?P<member_pk>\d+)/$', contribution_views.edit_for_member,
        name='edit-contributions-for-member'),
    url(r'^create/(?P<member_pk>\d+)/$', contribution_views.create_contribution, name='create-contribution'),
]
