from django import forms
from .models import Client, Applicant, Recruiter

skills = (('Java', 'Java'), ('C/C++','C/C++'), ('Go', 'Go'), ('JavaScript', 'JavaScript'), ('Python', 'Python'),
          ('Lua', 'Lua'), ('Shell', 'Shell'), ('PHP', 'PHP'), ('MySQL', 'MySQL'), ('Android', 'Android'))

class ClientSignupForm(forms.ModelForm):

    password = forms.CharField(widget= forms.PasswordInput)

    class Meta:
        model = Client
        exclude = ['user']

class ClientLoginForm(forms.Form):

    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget= forms.PasswordInput)

class ApplicantSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Applicant
        exclude = ['user', 'skills', 'resume_file']

class ApplicantLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

class NewPostingForm(forms.Form):

    job_title = forms.CharField(max_length=100)
    skills = forms.MultipleChoiceField( required=True, widget= forms.CheckboxSelectMultiple,
                                        choices= skills
    )

class ManagerLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

class NewRecruiterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Recruiter
        exclude = ['user']

class RecruiterLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

class UploadResumeForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()