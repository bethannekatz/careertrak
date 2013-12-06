from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse

from careerapp.models import *
from careerapp.forms import *

# Used to send mail from within Django
from django.core.mail import send_mail

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator


# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Needed to manually create HttpResponses or raise an Http404 exception
from django.http import HttpResponse, Http404

from django.contrib.sites.models import get_current_site

from django.db import transaction





# Reset the state of the database

@transaction.commit_on_success
def resetdb(request):

        # Delete all users
        User.objects.all().delete()

        # Delete Companies
        Company.objects.all().delete()
        JobListing.objects.all().delete()

        # Delete Schools
        School.objects.all().delete()
        
        Transcript.objects.all().delete()
        Letter.objects.all().delete()

        Connection.objects.all().delete()


        # Re - Add Schools and Companies
        school1 = School(name="Carnegie Mellon University", email="cmu.edu")
        school2 = School(name="Harvey Mudd", email="hmc.edu")
        school3 = School(name="MIT", email="mit.edu")
        school1.save()
        school2.save()
        school3.save()

        company1 = Company(name="Google", location="Mountain View, CA")
        company2 = Company(name="Goldman Sachs", location="New York City, NY")
        company3 = Company(name="Microsoft",location="Seattle, WA")
        company1.save()
        company2.save()
        company3.save()

        

        # Create default users

        # Students
        # 1 - username : athanikk@andrew.cmu.edu , password :  a, school : Carnegie Mellon University (Ajmal Thanikkal)
        # 2 - username : bkatz@andrew.cmu.edu , password :  b, school : Carnegie Mellon University (Beth Anne Katz)

        # Recruiters

        # 1 - username: recruiter1@mailinator.com, password: r1, company = Google
        # 2 - username: recruiter2@mailinator.com, password: r2, company = Goldman Sachs
        # 3 - username: recruiter3@mailinator.com, password: r3, company = Microsoft
        


        # 1 - username : athanikk@mit.edu , password :  a, school : MIT (Ajmal Thanikkal)
        new_user = User.objects.create_user(username = 'athanikk@andrew.cmu.edu',
                                        first_name='Ajmal',
                                        last_name='Thanikkal',
                                        password='a',
                                        email = 'athanikk@andrew.cmu.edu')

        new_user.is_active = True
        new_user.save()
        new_student = UserProfile(user = new_user, userType = UserProfile.STUDENT)
        new_student.school = school1
        new_student.save()

        # 2 
        new_user = User.objects.create_user(username = 'bkatz@andrew.cmu.edu',
                                        first_name='Beth Anne',
                                        last_name='Katz',
                                        password='b',
                                        email = 'bkatz@andrew.cmu.edu')

        new_user.is_active = True
        new_user.save()
        new_student = UserProfile(user = new_user, userType = UserProfile.STUDENT)
        new_student.school = school1
        new_student.save()

        # Recruiters

        #1
        new_user = User.objects.create_user(username = 'recruiter1@mailinator.com',
                                        first_name='Jack',
                                        last_name='Black',
                                        password='r1',
                                        email = 'recruiter1@mailinator.com')

        new_user.is_active = True
        new_user.save()
        new_r = UserProfile(user = new_user, userType = UserProfile.RECRUITER)
        new_r .company = company1
        new_r .save()

        #2
        new_user = User.objects.create_user(username = 'recruiter2@mailinator.com',
                                        first_name='Dana',
                                        last_name='FooPerson',
                                        password='r2',
                                        email = 'recruiter2@mailinator.com')

        new_user.is_active = True
        new_user.save()
        new_r = UserProfile(user = new_user, userType = UserProfile.RECRUITER)
        new_r .company = company2
        new_r .save()

         #3
        new_user = User.objects.create_user(username = 'recruiter3@mailinator.com',
                                        first_name='Marky',
                                        last_name='Mark',
                                        password='r3',
                                        email = 'recruiter2@mailinator.com')

        new_user.is_active = True
        new_user.save()
        new_r = UserProfile(user = new_user, userType = UserProfile.RECRUITER)
        new_r .company = company3
        new_r .save()               

        return redirect("/")
        
