from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'career_trak.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', 'careerapp.views.test'),
)
