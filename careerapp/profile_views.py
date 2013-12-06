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

@login_required		
def add_profile_pic(request):
        context ={}
        context['pg_user'] = request.user 
	if request.method == "GET":
		context = {'form':PhotoForm()}
		return render(request, 'careerapp/trueprofile.html', context)
	
	# else if POST request
	new_photo = Photo(user=request.user)
	form = PhotoForm(request.POST, request.FILES, instance=new_photo)
	if not form.is_valid():
		context = {'form':form}
		return render(request, 'careerapp/trueprofile.html', context)
		
	form.save()
	return redirect('true-profile', request.user.id)

def add_company_pic(request):
        context = {}
        user = request.user
        userProf = UserProfile.objects.get(user=user)
        context['company'] = userProf.company
        if request.method == "GET":
                context = {'form':PhotoForm()}
                return render(request, 'careerapp/companyProfile.html', context)

        # else if POST request
        print "Company: "
        print userProf.company.name
        new_photo = Photo(user=request.user, company=userProf.company)
        form = PhotoForm(request.POST, request.FILES, instance=new_photo)
        if not form.is_valid():
                context = {'form':form}
                return render(request, 'careerapp/companyProfile.html', context)
        form.save()
        return redirect('careerapp.navigation_views.companyPage', userProf.company.id)
	
@login_required
def add_transcript(request):
        context ={}
        context['pg_user'] =request.user 
	if request.method == "GET":
		context = {'form':TranscriptForm()}
		return render(request, 'careerapp/trueprofile.html', context)
		
	# else if POST request
	new_transcript = Transcript(user=request.user)
	form = TranscriptForm(request.POST, request.FILES, instance=new_transcript)
	print form.errors
	if not form.is_valid():
		context = {'form':form}
		return render(request, 'careerapp/trueprofile.html', context)
		
@login_required
def add_letter(request):
        context ={}
        context['pg_user'] =request.user 
	if request.method == "GET":
		context = {'form':LetterForm()}
		return render(request, 'careerapp/trueprofile.html', context)
		
	# else if POST request
	new_letter = Letter(user=request.user)
	form = LetterForm(request.POST, request.FILES, instance=new_letter)
	print form.errors
	if not form.is_valid():
		context = {'form':form}
		return render(request, 'careerapp/trueprofile.html', context)
	
	form.save()
	return redirect('true-profile', request.user.id)

@login_required
def get_photo(request, id):
        print "in get photo"
	entry = get_object_or_404(Photo, id=id)
	if not entry.picture:
		raise Http404
		
	content_type = guess_type(entry.picture.name)
	return HttpResponse(entry.picture, mimetype=content_type)

@login_required
def get_transcript(request, id):
	entry = get_object_or_404(Transcript, id=id)
	if not entry.transcript:
		raise Http404
		
	content_type = guess_type(entry.transcript.name)[0]
	print content_type
	return HttpResponse(entry.transcript, mimetype=content_type)
	
@login_required
def get_letter(request, id):
	entry = get_object_or_404(Letter, id=id)
	if not entry.letter:
		raise Http404
		
	content_type = guess_type(entry.letter.name)[0]
	print content_type
	return HttpResponse(entry.letter, mimetype=content_type)

# helper function to truncate floats
def trunc(f, n):
    slen = len('%.*f' % (n, f))
    return str(f)[:slen]

@login_required
@transaction.commit_on_success
def rating(request, companyID):
        if ('rating' in request.POST and request.POST['rating'] and
            request.POST['rating'].isdigit()):
                        rating = int(request.POST.get('rating', False))
                        company = Company.objects.get(pk=companyID)
                        oldNumRated = company.numRated
                        company.numRated += 1
                        floatNum = float((company.rating*oldNumRated + int(rating))/company.numRated)
                        floatNum = trunc(floatNum, 2)
                        company.rating = floatNum
                        company.save()
                        # figure out why this isn't doing reverse
                        return redirect('/company/' + str(companyID))
        else:
                message = "No rating selected. You must select a rating to vote."
                request.user.message_set.create(message = message)
                return redirect('/company/' + str(companyID))

@login_required
@transaction.commit_on_success
def true_profile(request, userID):
        pg_user = User.objects.get(pk = userID)

        photo = Photo.objects.filter(user = pg_user)
        context = {}
	# If a photo exists
	if len(photo) > 0:
                # grabbing last put-in photo
                photoIndex = len(photo) - 1
		context['photoID'] = photo[photoIndex].id
	transcript = Transcript.objects.filter(user=pg_user)	
	if len(transcript) > 0:
		context['transcriptID'] = transcript[0].id
	letter = Letter.objects.filter(user=pg_user)
	if len(letter) > 0:
		context['letterID'] = letter[0].id

        userProfile = pg_user.userProfile
        context['pg_user'] = pg_user
	context['school']       = userProfile.school
	context['company']      = userProfile.company

        if (userProfile.userType == UserProfile.STUDENT):
                context['isStudent'] = 'true'
        if (userProfile.userType == UserProfile.RECRUITER):
                context['isRecruiter'] = 'true'

        if (pg_user == request.user):
                context['canEdit'] = 'caneditexists'
                context['connectrequests'] = request.user.userProfile.connectRequests.all()
                context['connections'] = request.user.userProfile.connections.all()

        if (request.user in pg_user.userProfile.connectRequests.all()):
                context['pendingRequest'] = 'pending'

        if( pg_user.userProfile.userType != request.user.userProfile.userType):
                if(pg_user not in request.user.userProfile.connectRequests.all()):
                        context['canRequest'] = 'canRequest'

        #elif  (pg_user.userProfile.userType != request.user.userProfile.userType):
                #context['canConnect'] = 'canConnect'
                        

        

	return render(request, 'careerapp/trueprofile.html', context)

@login_required
def profile(request):
        return redirect('true-profile', request.user.id)
	
def companyProfile(request):
	context = {}
	return render(request, 'careerapp/companyProfile.html', context)

@login_required
@transaction.commit_on_success
def editProfile(request):
	if request.method == 'GET':
                context = {}
                user = request.user
                userProfile = UserProfile.objects.get(user=user)
		context['profile'] = userProfile
		return render(request, 'careerapp/editProfile.html', context)
	
	userProfile = UserProfile.objects.get(user=request.user)
	
	if 'location' in request.POST or request.POST['location']:
		userProfile.location = request.POST['location']
		userProfile.save()
		
	if 'industry' in request.POST or request.POST['industry']:
		userProfile.industry = request.POST['industry']
		userProfile.save()
	
	if 'degree' in request.POST or request.POST['degree']:
		userProfile.degree = request.POST['degree']
		userProfile.save()
	
	if 'currJobs' in request.POST or request.POST['currJobs']:
		userProfile.currJobs = request.POST['currJobs']
		userProfile.save()
		
	if 'prevJobs' in request.POST or request.POST['prevJobs']:
		userProfile.prevJobs = request.POST['prevJobs']
		userProfile.save()
	
	return redirect('true-profile/' + str(request.user.id))
