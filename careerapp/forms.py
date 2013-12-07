from django import forms

from django.contrib.auth.models import User
from models import *


class JobListingForm(forms.ModelForm):
	class Meta:
		model = JobListing
		exclude = ('company',)

		


class StudentRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length = 30,
                                label="",
                                widget = forms.TextInput(attrs={'class': 'form-control form-padding', 'placeholder':'First name'}))

    last_name = forms.CharField(max_length = 30,
                                label="",
                                widget = forms.TextInput(attrs={'class': 'form-control form-padding', 'placeholder': 'Last name'}))
                                
    password1 = forms.CharField(max_length = 30,
                                label="",
                                widget = forms.PasswordInput(attrs={'class': 'form-control form-padding', 'placeholder': 'Password'}))

    password2 = forms.CharField(max_length = 30,
                                label="",
                                widget = forms.PasswordInput(attrs={'class': 'form-control form-padding', 'placeholder': 'Confirm password'}))

    emailaddress = forms.CharField(max_length = 200,
                                label="",   
                                widget = forms.TextInput(attrs={'class': 'form-control form-padding', 'placeholder': 'School email address'}))

    school = forms.ModelChoiceField(queryset=School.objects.all().order_by('name'),
                                    label="School",
                                    widget = forms.Select(attrs={'class': 'form-control form-padding', 'placeholder': 'School'}))

    #Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(StudentRegistrationForm, self).clean()

        # Confirm that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        email = cleaned_data.get('emailaddress')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords must match.")

        print 'before'
        school = cleaned_data.get('school')
        print email

        if not school:
            raise forms.ValidationError("No school selected")

        # TODO : Write a better function
        if (school.email
            not in email):
             raise forms.ValidationError("Your email address does not match your school's")

        if(User.objects.filter(email=email)):
           raise forms.ValidationError("An account with this email address has already been registered")

        # Return the cleaned data we got from our parent.
        return cleaned_data
		
# USE ONE_TO_ONE 
class PhotoForm(forms.ModelForm):
	class Meta:
		model = Photo
		exclude = ('user', 'company')
		widgets = {'picture' : forms.FileInput() }
		
class TranscriptForm(forms.ModelForm):
	class Meta:
		model = Transcript
		exclude = ('user', )
		widgets = {'transcript' : forms.FileInput() }
		
class LetterForm(forms.ModelForm):
	class Meta:
		model = Letter
		exclude = ('user', )
		widgets = {'letter' : forms.FileInput() }

class ExperienceForm(forms.ModelForm):
        class Meta:
                model = Experience
                exclude = ('user', )

class RecruiterRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length = 30,
                                label="",
                                widget = forms.TextInput(attrs={'class': 'form-control form-padding', 'placeholder':'First name'}))

    last_name = forms.CharField(max_length = 30,
                                label="",
                                widget = forms.TextInput(attrs={'class': 'form-control form-padding', 'placeholder': 'Last name'}))
                                
    password1 = forms.CharField(max_length = 30,
                                label="",
                                widget = forms.PasswordInput(attrs={'class': 'form-control form-padding', 'placeholder': 'Password'}))

    password2 = forms.CharField(max_length = 30,
                                label="",
                                widget = forms.PasswordInput(attrs={'class': 'form-control form-padding', 'placeholder': 'Confirm password'}))

    emailaddress = forms.EmailField(max_length = 200,
                                label="",   
                                widget = forms.TextInput(attrs={'class': 'form-control form-padding', 'placeholder': 'Email address'}))

    company = forms.ModelChoiceField(queryset=Company.objects.all().order_by('name'),
                                    label="Company",
                                    widget = forms.Select(attrs={'class': 'form-control form-padding', 'placeholder': 'Company'}))

    #Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RecruiterRegistrationForm, self).clean()

        # Confirm that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        email = cleaned_data.get('emailaddress')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords must match.")

        print 'before'
        company = cleaned_data.get('company')
        print email

        if not company:
            raise forms.ValidationError("No company selected")


        if(User.objects.filter(email=email)):
           raise forms.ValidationError("An account with this email address has already been registered")

        # Return the cleaned data we got from our parent.
        return cleaned_data   


class EmailResetPasswordForm(forms.Form):
    emailaddress = forms.EmailField(max_length = 200,
                                label='Enter the email address associated with your account',
                                widget = forms.TextInput(attrs={'class': 'form-control'}))

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(EmailResetPasswordForm, self).clean()
        email = cleaned_data.get('emailaddress')
        if not User.objects.filter(email__exact=email):
            print "no"
            raise forms.ValidationError("That email address was not found!")

        # Return the cleaned data we got from our parent.
        return cleaned_data

class EditPasswordForm(forms.Form):
        current = forms.CharField(max_length=30, label="", widget=forms.PasswordInput(attrs={'class': 'form-control form-padding', 'placeholder': 'Current Password'}))
        password1 = forms.CharField(max_length=30, label="",widget=forms.PasswordInput(
                attrs={'class': 'form-control form-padding', 'placeholder': 'New password'}))
        password2 = forms.CharField(max_length=30, label="", widget=forms.PasswordInput(
                attrs={'class': 'form-control form-padding', 'placeholder': 'Confirm new password'}))
        # Customizes form validation for properties that apply to more
        # than one field.  Overrides the forms.Form.clean function.
        def clean(self):
                cleaned_data = super(EditPasswordForm, self).clean()
                password1 = cleaned_data.get('password1')
                password2 = cleaned_data.get('password2')
                if password1 and password2 and password1 != password2:
                        raise forms.ValidationError("Passwords must match.")
                return cleaned_data
