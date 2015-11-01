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
import cnto_notes.views as note_views
from django.conf.urls import include, url


urlpatterns = [
    url(r'^delete/(?P<note_pk>\d+)/$', note_views.delete_note, name='delete-note'),
    url(r'^edit-collection/(?P<member_pk>\d+)/$', note_views.edit_note_collection, name='edit-note-collection'),
    url(r'^edit/(?P<note_pk>\d+)/$', note_views.edit_note, name='edit-note'),
    url(r'^create/(?P<member_pk>\d+)/$', note_views.create_note, name='create-note'),
    url(r'^activate-note/(?P<pk>\d+)/$', note_views.activate_note, name='activate-note'),
]
