from django.conf.urls import patterns, include, url

# Used to send mail from within Django
from django.core.mail import send_mail

# Helper function to guess a MIME type from a file name
from mimetypes import guess_type

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

        # initialization
        url(r'^resetdb$', 'careerapp.init_views.resetdb'),
        url(r'^loadschools$', 'careerapp.account_views.loadschools'),

        ########################
        #  Account Management  #
        ########################
        url(r'^$', 'careerapp.account_views.loginpage'),
        url(r'^logoutLogin$', 'careerapp.account_views.loginpage',name='logoutLogin'),
	url(r'^frontpage$', 'careerapp.account_views.loginpage', name='frontpage'),
	url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'careerapp/loginpage.html'}, name='signin'),	
        url(r'^reset-password$', 'careerapp.account_views.reset_password', name='resetpassword'),
        url(r'^handle-reset-password/(?P<username>[^/]+)/(?P<token>[a-z0-9\-]+)$', 'careerapp.account_views.handle_reset_password'),
        url(r'^account$', 'careerapp.account_views.account', name='account'),
        url(r'^editpassword$', 'careerapp.account_views.edit_password', name = 'editpassword'),
	url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page':'logoutLogin'}, name='logout'),       
        url(r'^confirm/(?P<username>[^/]+)/(?P<token>[a-z0-9\-]+)$', 'careerapp.account_views.confirm_registration', name='confirm'),
        url(r'^register-student$', 'careerapp.account_views.register_student', name='register-student'),
        url(r'^register-recruiter$', 'careerapp.account_views.register_recruiter', name='register-recruiter'),
        url(r'^just-registered$', 'careerapp.account_views.just_registered', name='just_registered'),

        ########################
        #  Profile Management  #
        ########################
        url(r'^profile$', 'careerapp.profile_views.profile', name='profile'),
        url(r'^true-profile/(?P<userID>[0-9_@\+\-]+)$', 'careerapp.profile_views.true_profile', name='true-profile'),
	url(r'^edit-profile$', 'careerapp.profile_views.editProfile', name='edit'),
  	url(r'^add-photo$', 'careerapp.profile_views.add_profile_pic', name='add-photo'),
  	url(r'^add-company-photo$', 'careerapp.profile_views.add_company_pic', name='add-company-photo'),
	url(r'^get-photo/(?P<id>\d+)$', 'careerapp.profile_views.get_photo', name='get-photo'),
	url(r'^add-transcript$', 'careerapp.profile_views.add_transcript', name='add-transcript'),
	url(r'^get-transcript/(?P<id>\d+)$', 'careerapp.profile_views.get_transcript', name='get-transcript'),
	url(r'^add-letter$', 'careerapp.profile_views.add_letter', name='add-letter'),
	url(r'^get-letter/(?P<id>\d+)$', 'careerapp.profile_views.get_letter', name='get-letter'),
	url(r'^rating/(?P<companyID>[0-9_@\+\-]+)$', 'careerapp.profile_views.rating', name='rating'),



        ########################
        #   Site Navigation    #
        ########################
        url(r'^request-connect/(?P<userID>[0-9_@\+\-]+)$', 'careerapp.navigation_views.request_connection', name='request-connect'),
        url(r'^accept-connect/(?P<userID>[0-9_@\+\-]+)$', 'careerapp.navigation_views.accept_connection', name='accept'),
	url(r'^follow/(?P<companyID>[a-zA-Z0-9_@\+\-]+)', 'careerapp.navigation_views.follow', name='follow'),
	url(r'^company/(?P<companyID>[0-9_@\+\-]+)$', 'careerapp.navigation_views.companyPage', name='company'),
        url(r'^post-job/(?P<companyID>[0-9_@\+\-]+)$', 'careerapp.navigation_views.post_job', name='post-job'),
        url(r'^career-stream$', 'careerapp.navigation_views.career_stream', name='careerstream'),
        url(r'^search$', 'careerapp.navigation_views.search', name='search'),
        url(r'^jobposting/(?P<jobID>[0-9_@\+\-]+)$', 'careerapp.navigation_views.jobPosting', name='jobPosting')

)
