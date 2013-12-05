from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse

from careerapp.models import *
from careerapp.forms import *

# Used to send mail from within Django
from django.core.mail import send_mail

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Helper function to guess a MIME type from a file name
from mimetypes import guess_type

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Needed to manually create HttpResponses or raise an Http404 exception
from django.http import HttpResponse, Http404

from django.contrib.sites.models import get_current_site

from django.db import transaction

# show job listings from companies this user follows



#show the log in page
def loginpage(request):
        context = {}
        if request.method == 'GET':
   
                return render(request, 'careerapp/loginpage.html', {})

# When user clicks on reset password
@transaction.commit_on_success
def reset_password(request):
        context = {}
        if request.method == 'GET':
                context['form'] = EmailResetPasswordForm(auto_id=False)
                return render(request, 'careerapp/password_reset_form.html', context)

        
        form = EmailResetPasswordForm(request.POST)
        context['form'] = form


        # Checks the validity of the form data
        if not form.is_valid():
                return render(request, 'careerapp/password_reset_form.html', context)


        cleaned_data = form.cleaned_data
        email = cleaned_data.get('emailaddress')
    
        reset_user = User.objects.get(email__exact=email)
        print reset_user.username
        
        # Generate a one-time use token and an email message body
        token = default_token_generator.make_token(reset_user)
        print token
        

        recip_list = []
        recip_list.append(email)
        send_mail(subject ="Welcome to CareerTrak!",
              message = 'Click this link to reset'+
              'your password to the following temporary one:' + str(token)+ '\n'+ 'localhost:8000/handle-reset-password/'+str(reset_user.username)+'/'+str(token),
              from_email = 'athanikk@andrew.cmu.edu',
              recipient_list = recip_list)

        return redirect('/')

@transaction.commit_on_success
def handle_reset_password(request, username, token):
        user = get_object_or_404(User,username=username)
        # Send 404 error if token is invalid
        print 'passed'
        print user.username
        print token
        if not default_token_generator.check_token(user, token):
                raise Http404

        user.set_password(token)
        user.save()

        return redirect('/')

# Display the user account page
@login_required
def account(request):
        context = {}
        return render(request, 'careerapp/account.html', context)

@login_required
@transaction.commit_on_success
def edit_password(request):
        context = {}
        if request.method == 'GET':
                context['form'] = EditPasswordForm(auto_id=False)
                return render(request, 'careerapp/password_change_form.html', context)        

        form = EditPasswordForm(request.POST)
        context['form'] = form
        # Checks the validity of the form data
        if not form.is_valid():
                return render(request, 'careerapp/password_change_form.html', context)

        # Change the password
        old_password = form.cleaned_data['current']
        user = request.user

        if not user.check_password(old_password):
                raise Http404
        

        user.set_password(form.cleaned_data.get('password1'))
        user.save()

        return redirect('account')       

# Handle when the user clicks on the link from the email
@transaction.commit_on_success
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return redirect('true-profile', user.id)

# Display and process requests for the student registration page/form
@transaction.commit_on_success
def register_student(request):
        context = {}
        print "REGISTER STUDENT"
        if request.method == 'GET':
                context['form_r'] = StudentRegistrationForm(auto_id=False)
                print "REQUEST GET"
                return render(request, 'careerapp/student-register.html', context)

        print "REQUEST POST"

        form = StudentRegistrationForm(request.POST)
        context['form_r'] = form
        if not form.is_valid():
                print "INVALID"
                return render(request, 'careerapp/student-register.html', context)

        print "VALID"

        email_addr = form.cleaned_data['emailaddress']
        username_ = form.cleaned_data['emailaddress']
        new_user = User.objects.create_user(username = username_,
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        password=form.cleaned_data['password1'],
                                        email = email_addr)

        school = School.objects.get(name=form.cleaned_data['school'])
        
        
        new_user.is_active = True
        new_user.save()
        new_student = UserProfile(user = new_user, userType = UserProfile.STUDENT)
        new_student.school =  school
        new_student.save()


        # Send confirmation email

        # Generate a one-time use token and an email message body
        token = default_token_generator.make_token(new_user)
        

        recip_list = []
        recip_list.append(email_addr)
        send_mail(subject ="Welcome to CareerTrak!",
              message = 'Click this link to complete'+
              'the registration process: localhost:8000/confirm/'+str(username_)+'/'+str(token),
              from_email = 'athanikk@andrew.cmu.edu',
              recipient_list = recip_list)        
        
        return redirect('just_registered')


# Display and process requests for the recruiter registration page/form
@transaction.commit_on_success
def register_recruiter(request):
        context = {}
        print "REGISTER RECRUITER"
        if request.method == 'GET':
                context['form_r'] = RecruiterRegistrationForm(auto_id=False)
                print "REQUEST GET"
                return render(request, 'careerapp/recruiter-register.html', context)

        print "REQUEST POST"  
        form = RecruiterRegistrationForm(request.POST)
        context['form_r'] = form
        if not form.is_valid():
                print "INVALID"
                return render(request, 'careerapp/recruiter-register.html', context)

        print "valid"

        email_addr = form.cleaned_data['emailaddress']
        username_ = form.cleaned_data['emailaddress']
        new_user = User.objects.create_user(username = username_,
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        password=form.cleaned_data['password1'],
                                        email = email_addr)

        company = Company.objects.get(name=form.cleaned_data['company'])
        new_user.is_active = True
        new_user.save()
        new_student = UserProfile(user = new_user, userType = UserProfile.RECRUITER)
        new_student.company = company
        new_student.save()
		
        # Generate a one-time use token and an email message body
        token = default_token_generator.make_token(new_user)

        recip_list = []
        recip_list.append(email_addr)
        send_mail(subject ="Welcome to CareerTrak!",
              message = 'Click this link to complete'+
              'the registration process: localhost:8000/confirm/'+str(username_)+'/'+str(token),
              from_email = 'athanikk@andrew.cmu.edu',
              recipient_list = recip_list)  
        
                   
        return redirect("just_registered")


        
def just_registered(request):
        context = {}
        return render(request, 'careerapp/confirmationpage.html', context)




# Testing method that reloads database with school information
@transaction.commit_on_success
def loadschools(request):
        context ={}
        #school1 = School(name="Carnegie Mellon University", email="cmu.edu")
        #school2 = School(name="Harvey Mudd", email="hmc.edu")
        #school3 = School(name="MIT", email="mit.edu")
        school1 = School(name="C", email="cmu.edu")
        school2 = School(name="H", email="hmc.edu")
        school3 = School(name="M", email="mit.edu")
        school1.save()
        school2.save()
        school3.save()

        company1 = Company(name="Google", location="Mountain View, CA")
        company2 = Company(name="Goldman Sachs", location="New York City, NY")
        company3 = Company(name="Microsoft",location="Seattle, WA")
        company1.save()
        company2.save()
        company3.save()

        return redirect("/")



@transaction.commit_on_success	
def my_password_reset(request):
	return password_reset(request, 'careerapp/password_reset_complete.html')


