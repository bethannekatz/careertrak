from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse

from careerapp.models import *
from careerapp.forms import *

from django.template import Library
register = Library()

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
	#delete old photo
        old_photos = Photo.objects.filter(user=request.user)
        for photo in old_photos:
                photo.delete()
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
        # delete old photo
        old_photos = Photo.objects.filter(company=userProf.company)
        for photo in old_photos:
                photo.delete()
        new_photo = Photo(company=userProf.company)
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
	#delete old transcript
        old_transcript = Transcript.objects.filter(user=request.user)
        for transcript in old_transcripts:
                transcript.delete()
	new_transcript = Transcript(user=request.user)
	form = TranscriptForm(request.POST, request.FILES, instance=new_transcript)
	print form.errors
	if not form.is_valid():
		context = {'form':form}
		return render(request, 'careerapp/trueprofile.html', context)
	form.save()
	return redirect('true-profile', request.user.id)
		
@login_required
def add_letter(request):
        context ={}
        context['pg_user'] =request.user 
	if request.method == "GET":
		context = {'form':LetterForm()}
		return render(request, 'careerapp/trueprofile.html', context)
		
	# else if POST request
	# delete old letters
        old_letter = Letter.objects.filter(user=request.user)
        for letter in old_letters:
                letter.delete()
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
                return redirect('/company/' + str(companyID))

@register.filter         
def get_range(value):
        return range(value)


@login_required
@transaction.commit_on_success
def true_profile(request, userID):
        pg_user = User.objects.get(pk = userID)

        experiences = Experience.objects.filter(user=request.user)

        photo = Photo.objects.filter(user = pg_user, company = None)
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
	context['experiences'] = experiences

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
        context = {}
        userProfile = request.user.userProfile
        print userProfile
	if request.method == 'GET':
                print "GOT HERE"
		form = EditProfileForm(instance=userProfile)
		print "SECOND"
		context['form'] = form
		return render(request, 'careerapp/editProfile.html', context)


        form = EditProfileForm(request.POST)
        context['form'] = form

        if not form.is_valid():
                return render(request, 'careerapp/editProfile.html', context)
	
	if 'location' in form.cleaned_data:
                userProfile.location = form.cleaned_data['location'];
		
	if 'major' in form.cleaned_data:
                userProfile.major = form.cleaned_data['major'];
	
	if 'background' in form.cleaned_data:
                userProfile.background = form.cleaned_data['background'];
	
	if 'degreelevel' in form.cleaned_data:
                userProfile.degreelevel =  form.cleaned_data['degreelevel'];

        userProfile.save()		
	

	return redirect('true-profile', request.user.id)

@login_required
@transaction.commit_on_success
def recruiterEdit(request):
        context = {}
        userProfile = request.user.userProfile
	if request.method == 'GET':
		form = RecruiterEditProfileForm(instance=userProfile)
		context['form'] = form
		return render(request, 'careerapp/recruiterEditProfile.html', context)


        form = RecruiterEditProfileForm(request.POST)
        context['form'] = form

        if not form.is_valid():
                return render(request, 'careerapp/editProfile.html', context)
	
	if 'location' in form.cleaned_data:
                userProfile.location = form.cleaned_data['location'];
	
	if 'background' in form.cleaned_data:
                userProfile.background = form.cleaned_data['background'];
	
	if 'schools' in form.cleaned_data:
                userProfile.schools =  form.cleaned_data['schools'];

        userProfile.save()		
	

	return redirect('true-profile', request.user.id)

@login_required
@transaction.commit_on_success
def addExperience(request):
        if request.method == 'GET':
                context = {'form' : ExperienceForm()}
                return render(request, 'careerapp/addExperience.html', context)

        # else if POST request
        new_experience = Experience(user = request.user)
        form = ExperienceForm(request.POST, instance = new_experience)
        if not form.is_valid():
                context = {'form' : form}
                return render(request, 'careerapp/addExperience.html', context)
        # if form is valid
        form.save()
        return redirect('true-profile', request.user.id)
