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

import cnto_notes.urls as note_urls
import cnto_users.urls as user_urls

from views import scrape, login_user, event, member, report, group, manage, absence
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/manage/')),
    url(r'^/', RedirectView.as_view(url='/manage/')),
    url(r'^home/', manage.home, name="home"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', login_user.login_user, name='login'),

    url(r'^event-browser/', event.event_browser, name='event-browser'),
    url(
        r'^scrape/(?P<event_type_name>\w+)/(?P<dt_string>\w{4}-\w{2}-\w{2})/(?P<start_hour>[0-9]{2})h/(?P<end_hour>[0-9]{2})h/$',
        scrape.scrape, name='scrape'),

    url(r'^view-event/([0-9]{4})/([0-9]{2})/([0-9]{2})/$', event.view_event, name='view-event'),
    url(r'^view-event/([0-9]{4})-([0-9]{2})-([0-9]{2})/$', event.view_event, name='view-event'),
    url(r'^delete-event/(\d+)/$', event.delete_event, name='delete-event'),
    url(r'^delete-event-type/(\d+)/$', event.delete_event_type, name='delete-event-type'),
    url(r'^edit-event-type/(?P<pk>\d+)/$', event.edit_event_type, name='edit-event-type'),
    url(r'^create-event-type/$', event.create_event_type, name='create-event-type'),

    url(r'^manage/$', manage.management, name='manage'),

    url(r'^delete-member/(\d+)/$', member.delete_member, name='delete-member'),
    url(r'^edit-member/(?P<pk>\d+)/$', member.edit_member, name='edit-member'),
    url(r'^edit-discharged-member/(?P<pk>\d+)/$', member.edit_discharged_member, name='edit-discharged-member'),
    url(r'^create-member/$', member.create_member, name='create-member'),
    url(r'^create-recruit/$', member.create_recruit, name='create-recruit'),

    url(r'^delete-group/(\d+)/$', group.delete_group, name='delete-group'),
    url(r'^edit-group/(?P<pk>\d+)/$', group.edit_group, name='edit-group'),
    url(r'^create-group/$', group.create_group, name='create-group'),

    url(r'^delete-absence/(?P<absence_pk>\d+)/$', absence.delete_absence, name='delete-absence'),
    url(r'^edit-absences/(?P<member_pk>\d+)/$', absence.edit_absences, name='edit-absences'),
    url(r'^edit-absence/(?P<absence_pk>\d+)/$', absence.edit_absence, name='edit-absence'),
    url(r'^create-absence/(?P<member_pk>\d+)/$', absence.create_absence, name='create-absence'),

    url(r'^download-month-csv/(?P<dt_string>\w{4}-\w{2}-\w{2})/$', report.download_report_for_month,
        name='download-month-csv'),
    url(r'^download-group-month-csv/(?P<dt_string>\w{4}-\w{2}-\w{2})/(?P<group_pk>\d+)/$',
        report.download_report_for_month, name='download-group-month-csv'),

    url(r'^report-main/$', report.report_main, name='report-main'),
    url(r'^get-report-body-for-month/(?P<month_string>\w{4}-\w{2})/$', report.get_report_body_for_month, name='get-report-body-for-month'),
    url(r'^get-summary-data/$', report.get_summary_data, name='get-summary-data'),

    url(r'^notes/', include(note_urls)),
    url(r'^users/', include(user_urls))

]
