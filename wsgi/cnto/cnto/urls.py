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
from django.views.generic.base import RedirectView

from views import scrape, login_user, event, member
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/event-browser/', permanent=True)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', login_user.login_user, name='login'),

    url(r'^event-browser/', event.event_browser, name='event-browser'),
    url(r'^scrape/(\w{4}-\w{2}-\w{2})/([0-9]{2})h/([0-9]{2})h/$', scrape.scrape, name='scrape'),

    url(r'^view-event/([0-9]{4})/([0-9]{2})/([0-9]{2})/$', event.view_event, name='view-event'),
    url(r'^delete-event/(\d+)/$', event.delete_event, name='delete-event'),

    url(r'^delete-member/(\d+)/$', member.delete_member, name='delete-member'),
    url(r'^edit-member/(\d+)/$', member.edit_member, name='edit-member'),
    url(r'^list-members/$', member.list_members, name='list-members'),
]
