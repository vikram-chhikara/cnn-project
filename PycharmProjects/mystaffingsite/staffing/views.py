from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from staffing.models import Client
from django.contrib.auth import authenticate, login, logout
from .forms import ClientSignupForm, ClientLoginForm, ApplicantSignupForm, ApplicantLoginForm, NewPostingForm, ManagerLoginForm, NewRecruiterForm, RecruiterLoginForm, UploadResumeForm
from .models import Client, Applicant, ApplicantSkill, JobPosting, JobPostingSkill, Recruiter
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, user_passes_test, login_required
from django.db.models import Q
from operator import or_
from functools import reduce

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine

import datetime
import PyPDF2
from pdfrw import PdfReader

#Global declarations
skills = ['Java', 'C/C++', 'Go', 'JavaScript', 'Python', 'Lua', 'Shell', 'PHP', 'MySQL', 'Android']

def landing(request):
    """Asks user about their role"""
    return render(request, 'staffing/landing.html')

def managerLogin(request):

    if request.method == 'POST':
        form = ManagerLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            manager = authenticate(username=username, password=password)
            try:
                mangr = manager.manager
            except:
                return redirect('staffing:managerLogin')

            if manager is not None and manager.is_active:
                login(request, manager)
                return HttpResponseRedirect(reverse('staffing:managerDashboard', args=(manager.manager.id,)))
            else:
                return render(request, 'staffing/managerLogin.html', {'form': form})

    else:
        form = ManagerLoginForm()
        return render(request, 'staffing/managerLogin.html', {'form':form})

def recruiterLogin(request):

    if request.method == 'POST':

        form = RecruiterLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            recruiter = authenticate(username=username, password=password)

            try:
                recr = recruiter.recruiter
            except:
                return redirect('staffing:recruiterLogin')

            if recruiter is not None and recruiter.is_active:
                login(request, recruiter)
                return HttpResponseRedirect(reverse('staffing:recruiterDashboard', args=(recruiter.recruiter.id,)))
            else:
                return render(request, 'staffing/recruiterLogin.html', {'form': form})

    else:
        form = RecruiterLoginForm()

        return render(request, 'staffing/recruiterLogin.html', {'form':form})

def recruiterDashboard(request, recruiter_id):

    if not request.user.is_authenticated:
        return redirect('staffing:recruiterLogin')

    try:
        recruiter = request.user.recruiter
    except:
        print("recruiter is none")
        return redirect('staffing:recruiterLogin')

    if request.method == 'POST':
        hello = "hi"
    else:
        job_postings = JobPosting.objects.all()
        applicants = Applicant.objects.all()

        return render(request, 'staffing/recruiterDashboard.html', {'job_postings':job_postings, 'applicants':applicants, 'recruiter':recruiter})

def searchJobPosting(request, recruiter_id):

    if not request.user.is_authenticated:
        return redirect('staffing:recruiterLogin')

    try:
        recruiter = request.user.recruiter

    except:
        return redirect('staffing:recruiterLogin')

    res = None

    if request.method == 'POST':

        search_string = request.POST['jobPosting_search']
        search_string = search_string.strip()
        anded_skills = search_string.split("or")

        ored_skills_temp = [x.split("and") for x in anded_skills]

        ored_skills = [[skill.replace(" ", "") for skill in skills] for skills in ored_skills_temp]

        res = JobPosting.objects.filter(reduce(or_, [ Q(skills__contains=skills) for skills in ored_skills]))

        return render(request, 'staffing/searchJobPosting.html', {'res':res, 'recruiter':recruiter})

    else:
        return render(request, 'staffing/searchJobPosting.html', {'res':res, 'recruiter':recruiter})

def searchApplicant(request, recruiter_id):


    if not request.user.is_authenticated:
        return redirect('staffing:applicantLogin')
    try:
        recruiter = request.user.recruiter

    except:
        return redirect('staffing:recruiterLogin')

    res = None

    if request.method == 'POST':

        search_string = request.POST['applicant_search']
        search_string = search_string.strip()
        anded_skills = search_string.split("or")

        ored_skills_temp = [x.split("and") for x in anded_skills]

        ored_skills = [[skill.replace(" ", "") for skill in skills] for skills in ored_skills_temp]
        print(ored_skills)
        res = Applicant.objects.filter(reduce(or_, [Q(skills__contains=skills) for skills in ored_skills]))

        print(res)
        return render(request, 'staffing/searchApplicant.html', {'res': res, 'recruiter':recruiter})


    else:
        return render(request, 'staffing/searchApplicant.html', {'res': res, 'recruiter':recruiter})

def managerDashboard(request, manager_id):

    if not request.user.is_authenticated:
        return redirect('staffing:managerLogin')

    try:
        manager = request.user.manager
    except:
        print("manager is None")
        return redirect('staffing:managerLogin')

    if request.method == 'POST':

        hello = "hi"

    else:

        recruiters = Recruiter.objects.all()
        return render(request, 'staffing/managerDashboard.html', {'recruiters':recruiters, 'manager': manager})

def newRecruiter(request, manager_id):

    if not request.user.is_authenticated:
        return redirect('staffing:managerLogin')

    try:
        manager = request.user.manager

    except:
        return redirect('staffing:managerLogin')

    if request.method == 'POST':

        form = NewRecruiterForm(request.POST)

        if form.is_valid():

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = User.objects.create_user(
                    username=username,
                    password=password
                )
            except :
                return HttpResponseRedirect(reverse('staffing:managerDashboard', args=(manager.id,)))

            recruiter = Recruiter.objects.create(
                user = user,
                first_name = first_name,
                last_name=last_name,
                phone_number=phone_number,
                email=email,
                username=username,
                password=password,
            )

        return HttpResponseRedirect(reverse('staffing:managerDashboard', args=(manager.id,)))

    else:
        form = NewRecruiterForm()

        return render(request, 'staffing/newRecruiter.html', {'form':form, 'manager':manager})

def editRecruiter(request, manager_id, recruiter_id):

    if not request.user.is_authenticated:
        return redirect('staffing:managerLogin')
    try:
        manager = request.user.manager

    except:
        return redirect('staffing:managerLogin')

    recruiter = get_object_or_404(Recruiter, id=recruiter_id)

    if request.method == 'POST':

        form = NewRecruiterForm(request.POST, instance=recruiter)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect(reverse('staffing:managerDashboard', args=(manager.id,)))
    else:
        form = NewRecruiterForm(None, instance=recruiter)

        return render(request, 'staffing/editRecruiter.html', {'form':form, 'recruiter':recruiter, 'manager':manager})

def removeRecruiter(request, recruiter_id):

    if not request.user.is_authenticated:
        return redirect('staffing:managerLogin')
    try:
        manager = request.user.manager

    except:
        return redirect('staffing:managerLogin')

    rec = Recruiter.objects.get(id=recruiter_id)
    username = rec.username
    User.objects.filter(username=username).delete()
    Recruiter.objects.filter(id=recruiter_id).delete()
    return HttpResponseRedirect(reverse('staffing:managerDashboard', args=(manager.id,)))


def clientSignupOrLogin(request):
    signup_form = ClientSignupForm()
    login_form = ClientLoginForm()

    if request.method == 'POST':

        #SIGNUP
        if request.POST.get('submit') == 'Signup':

            form = ClientSignupForm(request.POST)



            if form.is_valid():

                company_name = form.cleaned_data['company_name']
                location = form.cleaned_data['location']
                phone_number = form.cleaned_data['phone_number']
                email = form.cleaned_data['email']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = User.objects.create_user(
                    username= username,
                    password = password
                )

                client = Client.objects.create(
                    user = user,
                    username=username,
                    password=password,
                    company_name=company_name,
                    location = location,
                    phone_number = phone_number,
                    email = email
                    )
                login(request, user)
                # render dashboard
                return HttpResponseRedirect(reverse('staffing:clientDashboard', args=(client.id,)))

            else:                                                                       #not a valid form
                return render(request, 'staffing/clientSignupOrLogin.html',
                              {'signup_form': signup_form, 'login_form': login_form})

        # LOGIN
        else:   #authenticate and signin user
            form = ClientLoginForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                clientUser = authenticate(username=username, password=password)

                try:
                    cl = clientUser.client
                except:
                    return redirect('staffing:clientSignupOrLogin')

                if clientUser is not None and clientUser.is_active:
                    login(request, clientUser)
                    return HttpResponseRedirect(reverse('staffing:clientDashboard', args=(clientUser.client.id,)))
                else:
                    return render(request, 'staffing/clientSignupOrLogin.html',
                                  {'signup_form': signup_form, 'login_form': login_form})
    # GET Request
    else:
        return render(request, 'staffing/clientSignupOrLogin.html', {'signup_form': signup_form, 'login_form':login_form})

def applicantSignupOrLogin(request):

    signup_form = ApplicantSignupForm()
    login_form = ApplicantLoginForm()

    if request.method == 'POST':

        # SIGNUP
        if request.POST.get('submit') == 'signup':

            form = ApplicantSignupForm(request.POST)

            if form.is_valid():

                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                phone_number = form.cleaned_data['phone_number']
                email = form.cleaned_data['email']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = User.objects.create_user(
                    username=username,
                    password=password
                )

                applicant = Applicant.objects.create(
                    user=user,
                    first_name= first_name,
                    last_name = last_name,
                    username=username,
                    password=password,
                    phone_number=phone_number,
                    email=email
                )
                login(request, user)
                # render dashboard
                return HttpResponseRedirect(reverse('staffing:applicantDashboard', args=(applicant.id,)))

            else:  # not a valid form
                return render(request, 'staffing/applicantSignupOrLogin.html',
                              {'signup_form': signup_form, 'login_form': login_form})


        # LOGIN
        else:  # authenticate and signin user
            form = ApplicantLoginForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                applicant = authenticate(username=username, password=password)

                try:
                    app = applicant.applicant
                except:
                    return redirect('staffing:applicantSignupOrLogin')

                if applicant is not None and applicant.is_active:
                    login(request, applicant)
                    return HttpResponseRedirect(reverse('staffing:applicantDashboard', args=(applicant.applicant.id,)))
                else:
                    return render(request, 'staffing/applicantSignupOrLogin.html',
                                  {'signup_form': signup_form, 'login_form': login_form})
    # GET Request
    else:
        return render(request, 'staffing/applicantSignupOrLogin.html',
                      {'signup_form': signup_form, 'login_form': login_form})


#permission_required('staffing.view_client_dashboard', raise_exception=True)
#@user_passes_test(lambda u: u.has_perm('staffing.view_client_dashboard'), 'staffing:clientSignupOrLogin')
def clientDashboard(request, client_id):

    if not request.user.is_authenticated:
        return redirect('staffing:clientSignupOrLogin')

    try:
        client = request.user.client
    except:
        return redirect('staffing:clientSignupOrLogin')

    job_postings = JobPosting.objects.filter(client=client)

    #job_posting_skills = {}

    # for job_posting in job_postings:
    #     skills = JobPostingSkill.objects.filter(job_posting=job_posting).values_list('skill_text', flat=True)
    #     job_posting_skills[job_posting.title] = skills
        #job_posting_skills.append((job_posting.title, job_posting.jobPostingSkill_set))


    #return render(request, 'staffing/clientDashboard.html',{'job_posting_skills':job_posting_skills})
    return render(request, 'staffing/clientDashboard.html', {'job_postings': job_postings, 'client':client})




def applicantDashboard(request, applicant_id):

    if not request.user.is_authenticated:
        return redirect('staffing:applicantSignupOrLogin')

    try:
        applicant = request.user.applicant
    except:
        return redirect('staffing:applicantSignupOrLogin')

    #POST request
    if request.method == 'POST':

        #Form submission
        if request.POST.get('submit') == 'submit_form':

            selected_skills = request.POST.getlist('skills')
            applicant.skills = selected_skills
            applicant.save()
            return HttpResponseRedirect(reverse('staffing:applicantDashboard', args=(applicant.id,)))


        #File submission
        file_form = UploadResumeForm(request.POST, request.FILES)

        if file_form.is_valid():

            file = request.FILES['file']
            title = request.POST['title']

            # #pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            # text = pdfFileObj.extractText()

            applicant.resume_file = file
            applicant.save()
            pdfFileObj = open("/Users/vikramchhikara/PycharmProjects/mystaffingsite/media/"+str(applicant.resume_file), 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            pgObj = pdfReader.getPage(0)
            text = pgObj.extractText()
            content = text.split("!")

            for c in content:
                if "Skills" in c:
                    skill_str = c[7:]
                    skill_list = skill_str.replace(" ", "").strip("\n").split(",")

            applicant.skills = skill_list
            applicant.save()
            return HttpResponseRedirect(reverse('staffing:applicantDashboard', args=(applicant.id,)))

    #GET Request
    else:
        file_form = UploadResumeForm()
        return render(request, 'staffing/applicantDashboard.html', {'skills': skills, 'file_form':file_form, 'applicant':applicant})

    #return render(request, 'staffing/applicantDashboard.html', {'skills': skills})



def logoutView(request):

    logout(request)
    return render(request, 'staffing/landing.html')

def newPosting(request, client_id):

    if not request.user.is_authenticated:
        return redirect('staffing:clientSignupOrLogin')
    try:
        client = request.user.client
    except:
        return redirect('staffing:clientSignupOrLogin')

    if request.method == 'POST':                        #POST request

        new_posting_form = NewPostingForm(request.POST)

        if new_posting_form.is_valid():

            skills = request.POST.getlist('skills')

            client = request.user.client

            job_posting = JobPosting.objects.create(title= request.POST['job_title'],client= client, skills=skills)

            print(job_posting.skills)
            # for skill in skills:
            #     JobPostingSkill.objects.create(job_posting=job_posting, skill_text = skill)

            return redirect('staffing:clientDashboard')
    else:                                               #GET request
        new_posting_form = NewPostingForm()
        return render(request, 'staffing/newPosting.html', {'form': new_posting_form, 'client':client})