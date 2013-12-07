from django.db import models
# Create your models here.
from django.contrib.auth.models import User
import datetime

class SearchResult(models.Model):
    name = models.CharField(max_length=50)
    tagline = models.CharField(max_length=50)
    resultType = models.CharField(max_length=50)

class School(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=30)
    def __unicode__(self):
        return self.name



class Company(models.Model):
    name = models.CharField(max_length=100)
    rating = models.FloatField(max_length=100, default='0')
    numRated = models.IntegerField(max_length=100, default='0')
    location = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_tag(self):
        return self.location

    def get_resulttype(self):
        return "Company"
           

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userProfile')
    school = models.ForeignKey(School, blank=True, null=True)
    company = models.ForeignKey(Company, blank=True, null=True, related_name="company")
    following = models.ManyToManyField(Company, blank=True, related_name="following", through='FollowingCompany')
    connectRequests = models.ManyToManyField(User, blank=True, related_name="connectRequests")
    connections = models.ManyToManyField(User, blank=True, related_name="connections")
    location = models.CharField(max_length=50, blank=True)
    degree = models.CharField(max_length=50, blank=True)
    background = models.TextField(max_length=5000, blank=True)


    STUDENT = 'student'
    RECRUITER = 'recruiter'
    
    USER_TYPE_CHOICES = (
        (STUDENT, 'Student'),
        (RECRUITER, 'Recruiter'),
    )

    
    userType = models.CharField(max_length=20, choices = USER_TYPE_CHOICES, default = STUDENT)

    #TODO ask TA about syntax

    def is_student(self):
        return self.userType in (self.STUDENT)

    def is_recruiter(self):
        return self.userType in (self.RECRUITER)
    
    def __unicode__(self):
        return self.user.username

    def get_name(self):
        return self.user.first_name + " " +self.user.last_name

    def get_tag(self):
        if self.userType in (self.STUDENT):
            return "A student at "+ str(self.school)
        else:
            return "A recruiter at "+ str(self.company)
        

    def get_resulttype(self):
        return self.userType
		
class FollowingCompany(models.Model):
	company = models.ForeignKey(Company)
	userProfile = models.ForeignKey(UserProfile)

# Represents a connection, which may or may not be acceped by both parties
class Connection(models.Model):
	user = models.ForeignKey(User)
	userProfile = models.ForeignKey(UserProfile)
	isValid = models.BooleanField()

class Photo(models.Model):
	picture = models.ImageField(upload_to="profilePics", blank=True)
	user = models.ForeignKey(User, blank=True)
	company = models.ForeignKey(Company, blank=True, null=True)
	def __unicode__(self):
		return str(self.id)

class JobListing(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField(max_length = 5000)
    company = models.ForeignKey(Company, blank=False, related_name='postings')
    creation_time = models.DateTimeField(default=datetime.datetime.now, editable=False)

    location = models.CharField(max_length=75, blank=True)
    category = models.CharField(max_length=50, blank=True)
    division = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.title

    def get_resulttype(self):
        return "Job Posting"

    def get_name(self):
        return self.title

class Transcript(models.Model):
	transcript = models.FileField(upload_to="transcripts", blank=True)
	user = models.ForeignKey(User)
	
class Letter(models.Model):
	letter = models.FileField(upload_to="letters", blank=True)
	user = models.ForeignKey(User)

class Experience(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=5000, blank=False)
    user = models.ForeignKey(User)
    #current = models.BooleanField()

    def get_current_experience(self, user):
        return Experience.objects.filter(user=user, current=True)
        

##class CommonResume(models.Model):
##    experience = models.CharField(max_length=500)
##    skills = models.CharField(max_length=500)
##    gpa = models.CharField(max_length=4, blank=True)
##
##    def __unicode__(self):
##        return self.experience
##
### Represents a institute of higher education.
### Is a ForeignKey on StudentUser
##class School(models.Model):
##    name = models.CharField(max_length=80)
##    def __unicode__(self):
##        return self.name
##
##
### A company whose recruiters are registred on the site
##class Company(models.Model):
##    name = models.CharField(max_length=80)
##    
##    def __unicode__(self):
##        return self.name
##
### Represents a studentUser associated with an existing school and user
##class StudentUser(models.Model):
##    user = models.OneToOneField(User)
##    school = models.ForeignKey(School)
##    resume = models.OneToOneField(CommonResume)
##    
##    def __unicode__(self):
##	return self.user.username
##
### Represents a recruiterUser associated with an existing company and user
##class RecruiterUser(models.Model):
##    user = models.OneToOneField(User)
##    company = models.ForeignKey(Company)
##    school = models.ManyToManyField(School, blank = True)
##    def __unicode__(self):
##	return self.user.username  +" Company: " + self.company
##

##


