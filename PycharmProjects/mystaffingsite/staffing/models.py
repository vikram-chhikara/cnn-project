from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

class Client(models.Model):
    """Client model has one to many relationship with Job Posting Model"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete= models.CASCADE)
    company_name = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=70, unique=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)

    # class Meta:
    #     permissions = (
    #         ("view_client_dashboard", "Can view client dashboard"),
    #     )

    def __str__(self):
        return self.company_name

class JobPosting(models.Model):
    """Job Posting has two relationships:
    1. Many to one relationship with Client
    2. Many to many relationship with Tag"""

    title = models.CharField(max_length=20)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    skills = ArrayField(models.CharField(max_length=50), blank=True, null=True)

    def __str__(self):
        return self.client.company_name + " "+ self.title

class Applicant(models.Model):
    """Applicant has many to many relationship with Tag"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=70)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    skills = ArrayField(models.CharField(max_length=50), blank=True, null=True)
    resume_file =  models.FileField(upload_to="resume_files/%Y/%m/%d/", blank=True, null=True)

    # class Meta:
    #     permissions = (
    #         ("view_applicant_dashboard", "Can view applicant dashboard"),
    #     )

    def __str__(self):
        return self.first_name + self.last_name

# class Skill(models.Model):
#     """Tag has two relationships:
#     1. Many to many relationship with JobPosting
#     2. Many to many relationship with Applicant"""
#
#     skill_text = models.CharField(max_length=20)
#     job_postings = models.ManyToManyField(JobPosting, through='JobPostingSkill')
#     applicants = models.ManyToManyField(Applicant, through='ApplicantSkill')


class JobPostingSkill(models.Model):
    """Intermediate model between JobPosting and Tag"""
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    skill_text = models.CharField(max_length=20, null=True)
    # skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return self.job_posting.client.company_name + " " + self.job_posting.title + " " + self.skill_text

class ApplicantSkill(models.Model):
    """Intermediate model between Applicant and Tag"""
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    skill_text = models.CharField(max_length=20, null=True)
    # skill = models.ForeignKey(Skill, on_delete=models.CASCADE)



class Manager(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=70)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)

    # class Meta:
    #     permissions = (
    #         ("view_manager_dashboard", "Can view manager dashboard"),
    #         ("add_recruiters", "Can add recruiters"),
    #         ("remove_recruiter", "Can remove recruiters"),
    #     )

    def __str__(self):
        return self.first_name + self.last_name


class Recruiter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=70, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)

    # class Meta:
    #     permissions = (
    #         ("view_recruiter_dashboard", "Can view recruiter dashboard"),
    #     )

    def __str__(self):
        return self.first_name + self.last_name