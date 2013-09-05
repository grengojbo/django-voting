# -*- mode: python; coding: utf-8; -*-
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    (r'^$', views.api_root),
    url(r"^vote/(?P<app_label>[\w\.-]+)/(?P<model_name>\w+)/(?P<object_id>\d+)/(?P<direction>up|down|clear)/$",
        views.ItemVote.as_view(), name="voting_vote"),
    url(r"^vote/(?P<app_label>[\w\.-]+)/(?P<model_name>\w+)/$", views.ItemVoteView.as_view(), name="voting_vote_view"),
    url(r"^view/(?P<app_label>[\w\.-]+)/(?P<model_name>\w+)/$", views.ItemView.as_view(), name="voting_view"),
)
