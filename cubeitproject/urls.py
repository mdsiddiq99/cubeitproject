"""cubeitproject URL Configuration

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
from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = patterns('', 
    # url(r'^admin/', include(admin.site.urls)),
    # create user
    url(r'^user/$', 'users.views.create_user'),
    # create cube
    # list all cubes
    url(r'^user/(?P<user_id>[0-9]+)/cube/$', 'cubes.views.get_or_create_cubes'),
    # create content
    # list all contents
    url(r'^user/(?P<user_id>[0-9]+)/content/$', 'contents.views.get_or_create_contents'),
    # create cube content
    url(r'^user/(?P<user_id>[0-9]+)/cube/(?P<cube_id>[0-9]+)/content$', 'cubes.views.create_cube_content'),
    # delete cube content
    url(r'^user/(?P<user_id>[0-9]+)/cube/(?P<cube_id>[0-9]+)/content/(?P<content_id>[0-9]+)$', 'cubes.views.delete_cube_content'),
    # delete cube
    url(r'^user/(?P<user_id>[0-9]+)/cube/(?P<cube_id>[0-9]+)$', 'cubes.views.delete_cube'),
    # share cube
    url(r'^user/(?P<user_id>[0-9]+)/cube/(?P<cube_id>[0-9]+)/share/$', 'cubes.views.share_cube'),
    # share content
    url(r'^user/(?P<user_id>[0-9]+)/content/(?P<content_id>[0-9]+)/share/$', 'contents.views.share_content'),
    )
