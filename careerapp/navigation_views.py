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

from django.db.models import Q

# show job listings from companies this user follows

@login_required
def career_stream(request):
        context ={}

        user = request.user
        # Get all the companies that this student is following
        companies = user.userProfile.following.all()

        # Create a job posting, name, text and company (object)
        postings = []      

        for company in companies:
               c_postings = company.postings.all()
               print c_postings
               postings.extend(c_postings)

        context['postings'] = postings

        # passing all photos
        photos = Photo.objects.all()
        context['photos'] = photos
        
        return render(request, 'careerapp/companyfeed.html', context)

@login_required
@transaction.commit_on_success
def follow(request, companyID):
	realUser = request.user
	userProfile = UserProfile.objects.get(user=request.user)
	toFollow = Company.objects.get(pk=companyID)
	newFollow = FollowingCompany(company=toFollow, userProfile=userProfile)
	newFollow.save()
	return redirect('true-profile', request.user.id)


#Notify requested user by adding to their connectRequests
@login_required
@transaction.commit_on_success
def accept_connection(request, userID):
        acceptingUser = request.user
        requestingUser = User.objects.get(pk=userID)

        acceptingUser.userProfile.connectRequests.remove(requestingUser)

        acceptingUser.userProfile.connections.add(requestingUser)
        acceptingUser.save()
        requestingUser.userProfile.connections.add(acceptingUser)
        requestingUser.save()
        return redirect('true-profile', acceptingUser.id)


#Notify requested user by adding to their connectRequests
@login_required
@transaction.commit_on_success
def request_connection(request, userID):
        realUser = request.user
        toRequest = User.objects.get(pk=userID).userProfile
        toRequest.connectRequests.add(realUser)
        toRequest.save()
        return redirect('true-profile', toRequest.id)

@login_required
@transaction.commit_on_success
def companyPage(request, companyID):
	company = Company.objects.get(pk=companyID)
	jobs = JobListing.objects.filter(company=company)
	context = {'company':company}
	context['jobs'] = jobs
	photo = Photo.objects.filter(company = company)
	print photo
        # If a photo exists
	if len(photo) > 0:
                # grabbing last put-in photo
                photoIndex = len(photo) - 1
		context['photoID'] = photo[photoIndex].id
	return render(request, 'careerapp/companyProfile.html', context)

@login_required
def jobPosting(request, jobID):
        context ={}
        job = JobListing.objects.get(pk=jobID)
        context['job'] = job
        return render(request, 'careerapp/posting.html', context)
        
	
@login_required
@transaction.commit_on_success
def post_job(request, companyID):
        context ={}
        if request.method == 'GET':
                #cid = request.GET['companyid']
                cid = companyID
                company = Company.objects.get(pk=cid)
                context['company'] =company
                context['form'] = JobListingForm()
                return render(request, 'careerapp/post-job.html', context)

        form = JobListingForm(request.POST)

        context['form'] = form
        if not form.is_valid():
                print "INVALID"
                return render(request, 'careerapp/post-job.html', context)

        #cid = request.POST['companyid']
        cid = companyID
        company = Company.objects.get(pk=cid)

        listing = JobListing(title=form.cleaned_data['title'],
                             text=form.cleaned_data['text'],
                             company=company)

        if 'location' in form.cleaned_data:
                listing.location = form.cleaned_data['location']
        if 'category' in form.cleaned_data:
                listing.category = form.cleaned_data['category']
        if 'division' in form.cleaned_data:
                listing.division = form.cleaned_data['division']
        
        listing.save()

        # Why can't I redirect to a named url here?

	print cid
        return redirect('careerapp.navigation_views.companyPage', cid)

@login_required
def search(request):
        context={};
        if request.method == 'GET':
                return redirect('profile')

        q = request.POST['query']
        resultList = []
        companies = Company.objects.filter(
                Q(name__icontains=q))

        resultList.extend(companies)
        
        profiles = UserProfile.objects.filter(
                Q(school__name__icontains=q) | Q(user__first_name__icontains=q)
                | Q(user__last_name__icontains=q))

        resultList.extend(profiles)
        
        jlistings = JobListing.objects.filter(
                Q(title__icontains=q) | Q(location__icontains=q) | Q(category__icontains=q)
                | Q(text__icontains=q) | Q(company__name__icontains=q))
        
        resultList.extend(jlistings)

##        resultList.extend(Company.objects.filter(name__icontains=queryString))
##        resultList.extend(UserProfile.objects.filter(school__name__icontains=queryString))
##        resultList.extend(UserProfile.objects.filter(user__first_name__icontains=queryString))
##        resultList.extend(UserProfile.objects.filter(user__last_name__icontains=queryString))
##        resultList.extend(JobListing.objects.filter(title__icontains=queryString))
##        resultList.extend(JobListing.objects.filter(location__icontains=queryString))
##        resultList.extend(JobListing.objects.filter(category__icontains=queryString))
##        resultList.extend(JobListing.objects.filter(text__icontains=queryString))
##        resultList.extend(JobListing.objects.filter(company__name__icontains=queryString))
##
       
        context['results'] = resultList
        context['query'] = request.POST['query']

        # adding company photos
        photos = Photo.objects.all()
        context['photos'] = photos
        return render(request, 'careerapp/searchresults.html', context)
        

