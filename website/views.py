from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import User,Personal_Detail,Work_Detail,Contact_Detail,Experience_Detail,Bank_Detail,Paper_Publication,Patent,PHD_Awarded,Awards,Books,Books_Conference,CSV_Download
from datetime import date
from django.contrib import messages
import datetime

import os
import pandas as pd
import csv
# Create your views here.


def date_suffix(myDate):
    date_suffix = ["th", "st", "nd", "rd"]

    if myDate % 10 in [1, 2, 3] and myDate not in [11, 12, 13]:
        return date_suffix[myDate % 10]
    else:
        return date_suffix[0]
    
def current_date():
    today = date.today()
    current_day = today.day
    suffix = date_suffix(current_day)
    current = today.strftime('%A , %B %d')
    updated = str(current + suffix)
    return updated

def get_time_of_day():
    time = datetime.datetime.now().hour
    if time < 12:
        return "Morning"
    elif time < 16:
        return "Afternoon"
    elif time < 21:
        return "Evening"
    else:
        return "Night"

def profile(logged_user):
    score = 0
    empty_fields = []
    #check profile complete or not
    try:
        personal = Personal_Detail.objects.filter(user=logged_user).get()
        score += 20
    except:
        empty_fields.append('personal')
    try:
        work = Work_Detail.objects.filter(user=logged_user).get()
        score += 20
    except:
        empty_fields.append('work')
    try:
        contact = Contact_Detail.objects.filter(user=logged_user).get()
        score += 20
    except:
        empty_fields.append('contact')
    try:
        bank = Bank_Detail.objects.filter(user=logged_user).get()
        score += 20
    except:
        empty_fields.append('bank')
    try:
        experience = Experience_Detail.objects.filter(user=logged_user).get()
        score += 20
    except:
        empty_fields.append('experience')

    return score,empty_fields


def login_view(request):
    if request.method == "POST":
        aadhar = request.POST["aadhar"]
        password = request.POST["password"]
        user = authenticate(request, username=aadhar, password=password)
        
        # Check if authentication successful
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now Logged In.')
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "website/login.html", {
                "message": "Invalid username and/or password."
            })  
    else:
        return render(request, "website/login.html")
    
def login_view(request):
    if request.method == "POST":
        aadhar = request.POST["aadhar"]
        password = request.POST["password"]
        user = authenticate(request, username=aadhar, password=password)
        
        # Check if authentication successful
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now Logged In.')
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "website/login.html", {
                "message": "Invalid username and/or password."
            })  
    else:
        return render(request, "website/login.html")
    
def register_user(request):
    if request.method == "POST":

        #register details
        mail_id = request.POST["mail_id"]
        employer_id = request.POST["employer_id"]
        employer_name = request.POST["employer_name"]
        password = request.POST["password"]
        confirmation = request.POST["confirm_password"]
        aadhar = request.POST['aadhar']
        
        if password != confirmation:
            return render(request,'website/register.html',{
                'message':'Passwords Must Match'
            })
        
        try:
            user = User.objects.create_user(username=aadhar, email=mail_id, password=password)
            user.employee_code = employer_id
            user.employee_name = employer_name
            user.aadhar_number = aadhar
            
            user.save()

            messages.success(request, 'New User Registered Successfully')

            login(request, user)

            return HttpResponseRedirect(reverse("index"))

        except IntegrityError:
            return render(request, "website/register.html", {
                "message": "Existing User/AADHAR."
            })

    else:
        return render(request, "website/register.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse(login_view))

@login_required(login_url=login_view)
def index(request):
    current_user = request.user

    #check if user profile is complete or not
    score,empty_list = profile(current_user)

    if current_user.employee_code == 'admin':
        patents = len(Patent.objects.all())

        phds = len(PHD_Awarded.objects.all())

        papers = len(Paper_Publication.objects.all())

        awards = len(Awards.objects.all())

        books = len(Books.objects.all())

        books_conference = len(Books_Conference.objects.all())
    else:

        patents = len(Patent.objects.filter(user = current_user).all())

        phds = len(PHD_Awarded.objects.filter(user = current_user).all())

        papers = len(Paper_Publication.objects.filter(user = current_user).all())

        awards = len(Awards.objects.filter(user = current_user).all())

        books = len(Books.objects.filter(user = current_user).all())

        books_conference = len(Books_Conference.objects.filter(user = current_user).all())

    
    return render(request,'website/index.html',{
        'current_user' :current_user,
        'date': current_date(),
        'mor_eve' : get_time_of_day(),
        'empty_list':empty_list,
        'patents':patents,
        'phds' : phds,
        'papers': papers,
        'awards':awards,
        'books': books,
        'conference': books_conference,
        'score':score,
        'empty_list':empty_list
    })

@login_required(login_url=login_view)
def personal_details(request):
    if request.method == "POST":
        father_name = request.POST["father_name"]
        mother_name = request.POST["mother_name"]
        dateofbirth = request.POST["dateofbirth"]
        bloodgrp = request.POST["blood_group"]
        gender = request.POST["gender"]
        maritial_status = request.POST["maritial_status"]
        if maritial_status == 'Married':
            spouse_name = request.POST["spouse_name"]

        current_user = request.user

        try:
            details = Personal_Detail.objects.filter(user=current_user).get()
            details.father_name = father_name
            details.mother_name = mother_name
            details.maritial_status = maritial_status
            if maritial_status == 'Married':
                details.spouse_name = spouse_name
            details.date_of_birth = dateofbirth
            details.gender = gender
            details.blood_group = bloodgrp
            details.save()

            messages.success(request, 'Personal Details Updated.')
        except:
            personal = Personal_Detail()
            personal.user = current_user
            personal.father_name = father_name
            personal.mother_name = mother_name
            personal.maritial_status = maritial_status
            if maritial_status == 'Married':
                personal.spouse_name = spouse_name
            personal.date_of_birth = dateofbirth
            personal.gender = gender
            personal.blood_group = bloodgrp

            personal.save()

            messages.success(request, 'Personal Details Saved. ')
        
        #return kya karana yaha par
        return HttpResponseRedirect(reverse(personal_details))
        
    else:
        current_user = request.user
        score,empty_list = profile(current_user)
        try:
            details = Personal_Detail.objects.filter(user=current_user).get()
            return render(request,'website/personal.html',{
                'current_user' :current_user,
                'date': current_date(),
                'score':score,
                'empty_list':empty_list,
                'mor_eve' : get_time_of_day(),
                'father_name':details.father_name,
                'mother_name':details.mother_name,
                'maritial_status':details.maritial_status,
                'spouse_name':details.spouse_name,
                'date_of_birth':details.date_of_birth,
                'gender':details.gender,
                'blood_group':details.blood_group
            })
        except:
            return render(request,'website/personal.html',{
                'current_user' :current_user,
                'date': current_date(),
                'mor_eve' : get_time_of_day(),
                'message': 'Enter data'
            })
        
@login_required(login_url=login_view)
def work_details(request):
    if request.method == "POST":
        designation = request.POST["designation"]
        mode_of_recruitment = request.POST["mode_of_recruitment"]
        dob_joining = request.POST["dob_joining"]
        dob_retirement = request.POST["dob_retirement"]

        current_user = request.user

        try:
            details = Work_Detail.objects.filter(user=current_user).get()
            details.designation = designation
            details.mode_of_recruitment = mode_of_recruitment
            details.dob_joining = dob_joining
            details.dob_retirement = dob_retirement
            
            details.save()

            messages.success(request, 'Work Details Updated. ')
        except:
            work = Work_Detail()
            current_user = request.user
            work.user = current_user
            work.designation = designation
            work.mode_of_recruitment = mode_of_recruitment
            work.dob_joining = dob_joining
            work.dob_retirement = dob_retirement

            work.save()
            messages.success(request, 'Work Details Saved. ')
        
        return HttpResponseRedirect(reverse(work_details))
    else:
        current_user = request.user
        score,empty_list = profile(current_user)
        try:
            details = Work_Detail.objects.filter(user=current_user).get()
            return render(request,'website/work.html',{
                'current_user' :current_user,
                'date': current_date(),
                'score':score,
                'empty_list':empty_list,
                'mor_eve' : get_time_of_day(),
                'designation':details.designation,
                'mode_of_recruitment':details.mode_of_recruitment,
                'dob_joining':details.dob_joining,
                'dob_retirement':details.dob_retirement,
            })
        except:
            return render(request,'website/work.html',{
                'current_user' :current_user,
                'date': current_date(),
                'score':score,
                'empty_list':empty_list,
                'mor_eve' : get_time_of_day(),
                'message':'Enter data'
            })
        
@login_required(login_url=login_view)
def contact_details(request):
    if request.method=="POST":
        
        aadhar = request.POST["aadhar"]
        pan_number = request.POST["pan_number"]
        state = request.POST["state"]
        pincode = request.POST["pincode"]
        district = request.POST["district"]
        mobile = request.POST["mobile"]
        mobile_alt = request.POST["mobile_alternate"]
        landline = request.POST["landline"]
        corresponding_address = request.POST['corresponding_address']
        permanent_address = request.POST['permanent_address']


        try:
            details = Contact_Detail.objects.filter(user=request.user).get()
            details.aadhar = aadhar
            details.pan_number = pan_number
            details.state = state
            details.district = district
            details.pin = pincode
            details.mobile = mobile
            details.mobile_alt = mobile_alt
            details.landline = landline
            details.corresponding_address = corresponding_address
            details.permanent_address = permanent_address
            details.save()

            messages.success(request, 'Contact Details Updated. ')
        except:
            contact = Contact_Detail()
            current_user = request.user
            contact.user = current_user
            contact.aadhar = aadhar
            contact.pan_number = pan_number
            contact.state = state
            contact.district = district
            contact.pin = pincode
            contact.mobile = mobile
            contact.mobile_alt = mobile_alt
            contact.landline = landline
            contact.corresponding_address = corresponding_address
            contact.permanent_address = permanent_address
            contact.save()

            messages.success(request, 'Contact Details Saved. ')

        return HttpResponseRedirect(reverse(contact_details))

    else:
        current_user = request.user
        score,empty_list = profile(current_user)
        try:
            details = Contact_Detail.objects.filter(user=current_user).get()
            return render(request,'website/contact.html',{
                'current_user' :current_user,
                'date': current_date(),
                'mor_eve' : get_time_of_day(),
                'score':score,
                'empty_list':empty_list,
                'aadhar':details.aadhar,
                'pan_number':details.pan_number,
                'state':details.state,
                'district':details.district,
                'pincode':details.pin,
                'mobile':details.mobile,
                'mobile_alt':details.mobile_alt,
                'landline':details.landline,
                'corresponding_address':details.corresponding_address,
                'permanent_address':details.permanent_address,
            })
        except:
            return render(request,'website/contact.html',{
                'current_user' :current_user,
                'date': current_date(),
                'mor_eve' : get_time_of_day(),
                'score':score,
                'empty_list':empty_list,
                'message':'Enter data'
            })
        
@login_required(login_url=login_view)
def bank_details(request):
    if request.method=="POST":
        bank_name = request.POST["bank_name"]
        bank_account = request.POST["bank_account"]
        bank_ifsc = request.POST["ifsc_code"]
        bank_branch = request.POST["ifsc_code"]

        try:
            details= Bank_Detail.objects.filter(user=request.user).get()
            details.bank_name = bank_name
            details.bank_account = bank_account
            details.bank_ifsc = bank_ifsc
            details.bank_branch = bank_branch
            details.save()
            messages.success(request, 'Bank Details Saved. ')
        except:
            bank = Bank_Detail()
            bank.user = request.user
            bank.bank_name = bank_name
            bank.bank_account = bank_account
            bank.bank_ifsc = bank_ifsc
            bank.bank_branch = bank_branch
            bank.save()
            messages.success(request, 'Bank Details Updated. ')

        return HttpResponseRedirect(reverse(bank_details))


    else:
        current_user = request.user
        score,empty_list = profile(current_user)
        try:
            details = Bank_Detail.objects.filter(user=current_user).get()
            return render(request,'website/bank.html',{
                'current_user' :current_user,
                'date': current_date(),
                'mor_eve' : get_time_of_day(),
                'score':score,
                'empty_list':empty_list,
                'bank_name':details.bank_name,
                'bank_ifsc':details.bank_ifsc,
                'bank_account':details.bank_account,
                'bank_branch':details.bank_branch,
            })
        except:
            return render(request,'website/bank.html',{
                'current_user' :current_user,
                'date': current_date(),
                'mor_eve' : get_time_of_day(),
                'score':score,
                'empty_list':empty_list,
                'message':'Enter data'
            })
        
@login_required(login_url=login_view)
def experience_details(request):
    if request.method=="POST":
        teaching_exp = request.POST["teaching_experience"]
        industry_exp = request.POST["industry_experience"]
        research_exp = request.POST["research_experience"]
        teaching_exp_pup = request.POST["teaching_experience_pup"]

        try:
            details = Experience_Detail.objects.filter(user=request.user).get()
            details.teaching_experience = teaching_exp
            details.research_experience = research_exp
            details.industry_experience = industry_exp
            details.pup_teaching_experience = teaching_exp_pup
            details.save()
            messages.success(request, 'Experience Details Updated. ')
        except:
            experience = Experience_Detail()
            experience.user = request.user
            experience.teaching_experience = teaching_exp
            experience.research_experience = research_exp
            experience.industry_experience = industry_exp
            experience.pup_teaching_experience = teaching_exp_pup
            experience.save()

            messages.success(request, 'Experience Details Saved. ')

        return HttpResponseRedirect(reverse(experience_details))
        
    else:
        current_user = request.user
        score,empty_list = profile(current_user)
        try:
            details = Experience_Detail.objects.filter(user=current_user).get()
            return render(request,'website/experience.html',{
                'current_user' :current_user,
                'date': current_date(),
                'mor_eve' : get_time_of_day(),
                'score':score,
                'empty_list':empty_list,
                'teaching_experience':details.teaching_experience,
                'research_experience':details.research_experience,
                'industry_experience':details.industry_experience,
                'pup_teaching_experience':details.pup_teaching_experience,
            })
        except:
            return render(request,'website/experience.html',{
                'current_user' :current_user,
                'date': current_date(),
                'mor_eve' : get_time_of_day(),
                'score':score,
                'empty_list':empty_list,
                'message':'Enter data'
            })
        
@login_required(login_url=login_view)
def patent_register(request):
    if request.method == "POST":
        patent_number = request.POST["patent_number"]
        patent_title = request.POST["patent_title"]
        year_awarded = request.POST["year_awarded"]
        author_name = request.POST['author_name']
        category = request.POST['category']

        patent = Patent()
        patent.user = request.user
        patent.author_name = author_name
        patent.patent_number = patent_number
        patent.patent_title = patent_title
        patent.patent_year = year_awarded
        patent.category = category
        patent.save()

        messages.success(request, 'Patent Registered Successfully')

        return HttpResponseRedirect(reverse(patent_display))
    else:
        current_user=request.user
        score,empty_list = profile(current_user)
        return render(request,'website/patent.html',{
            'current_user': current_user,
            'mor_eve' : get_time_of_day(),
            'date': current_date(),
            'score':score,
            'empty_list':empty_list,
            
        })
    
@login_required(login_url=login_view)
def phd_awarded(request):
    if request.method == "POST":
        department = request.POST["department"]
        guide_names = request.POST["guide_names"]
        thesis_title = request.POST["thesis_title"]
        registration_date = request.POST["registration_date"]
        award_date = request.POST["award_date"]
        scholor_name = request.POST['scholor_name']

        phd = PHD_Awarded()
        phd.user = request.user
        phd.scholor_name = scholor_name
        phd.department = department
        phd.guide_names = guide_names
        phd.thesis_title = thesis_title
        phd.award_date = award_date
        phd.registration_date = registration_date
        phd.save()

        messages.success(request, 'Ph.D Registered Successfully')

        return HttpResponseRedirect(reverse(phd_display))

    else:
        current_user=request.user
        score,empty_list = profile(current_user)
        return render(request,'website/phd.html',{
            'current_user': current_user,
            'mor_eve' : get_time_of_day(),
            'date': current_date(),
            'score':score,
            'empty_list':empty_list,
        })
    
@login_required(login_url=login_view)
def research_publication(request):
    if request.method == "POST":
        title = request.POST["title"]
        author_names = request.POST["author_names"]
        journal_name = request.POST["journal_name"]
        journal_url = request.POST["journal_url"]
        issn = request.POST["issn"]
        publisher = request.POST["publisher"]
        month_published = request.POST["month_published"]
        year_published = request.POST["year_published"]
        volume_number = request.POST["volume_number"]
        issue_number = request.POST["issue_number"]
        pp = request.POST["pp"]
        doi = request.POST["doi"]
        ugc_core = request.POST["ugc_core"]
        scopus = request.POST["scopus"]
        sci_scie_esci = request.POST["sci_scie_esci"]
        if sci_scie_esci != 'None':
            impact_factor = request.POST["impact_factor"]

        paper = Paper_Publication()
        paper.user = request.user
        paper.title = title
        paper.author_names = author_names
        paper.journal_name = journal_name
        paper.journal_website = journal_url
        paper.issn = issn
        paper.publisher = publisher
        paper.month_published = month_published
        paper.year_published = year_published
        paper.volume_number = volume_number
        paper.issue_number = issue_number
        paper.pp = pp
        paper.doi = doi
        paper.ugc_core = ugc_core
        paper.scopus = scopus
        paper.sci_scie_esci = sci_scie_esci
        if sci_scie_esci != 'None':
            paper.impact_factor = impact_factor
        paper.save()

        return HttpResponseRedirect(reverse(research_display))
    else:
        current_user=request.user
        score,empty_list = profile(current_user)
        return render(request,'website/research.html',{
            'current_user': current_user,
            'mor_eve' : get_time_of_day(),
            'date': current_date(),
            'score':score,
            'empty_list':empty_list,
        })

@login_required(login_url=login_view)
def awards(request):
    if request.method == "POST":
        activity = request.POST["activity"]
        award_name = request.POST["award_name"]
        authority_name = request.POST["authority_name"]
        year_awarded = request.POST["year_awarded"]
        scholor_name = request.POST['scholor_name']
        level = request.POST['level']

        award = Awards()
        award.user = request.user
        award.scholor_name = scholor_name
        award.activity = activity
        award.award_name = award_name
        award.authority_name = authority_name
        award.year_awarded = year_awarded
        award.level = level
        award.save()

        return HttpResponseRedirect(reverse(award_display))
    else:
        current_user=request.user
        score,empty_list = profile(current_user)
        return render(request,'website/award.html',{
            'current_user': current_user,
            'mor_eve' : get_time_of_day(),
            'date': current_date(),
            'score':score,
            'empty_list':empty_list,
        })
    
@login_required(login_url=login_view)
def books(request):
    if request.method == "POST":
        author_name = request.POST["author_name"]
        book_title = request.POST["book_title"]
        publisher = request.POST["publisher"]
        isbn = request.POST["isbn"]
        year_published = request.POST["year_published"]
        affiliate_uni = request.POST['affiliate_uni']

        books = Books()
        books.user = request.user
        books.authors = author_name
        books.title = book_title
        books.publisher = publisher
        books.isbn = isbn
        books.year_published = year_published
        books.affiliating_institute = affiliate_uni
        books.save()

        return HttpResponseRedirect(reverse(books_display))
    else:
        current_user=request.user
        score,empty_list = profile(current_user)
        return render(request,'website/books.html',{
            'current_user': current_user,
            'date': current_date(),
            'mor_eve' : get_time_of_day(),
            'score':score,
            'empty_list':empty_list,
        })
    
@login_required(login_url=login_view)
def conference(request):
    if request.method == "POST":
        author_name = request.POST["author_name"]
        category = request.POST["category"]
        type = request.POST["type"]
        publisher = request.POST["publisher"]
        date = request.POST["date"]
        title_ch_paper = request.POST['title_ch_paper']
        title_book_conf = request.POST['title_book_conf']
        isbn = request.POST['isbn']
        pp = request.POST['pp']

        books_conf = Books_Conference()
        books_conf.user = request.user
        books_conf.authors = author_name
        books_conf.category = category
        books_conf.publisher = publisher
        books_conf.isbn = isbn
        books_conf.title_book_conf = title_book_conf
        books_conf.title_chap_paper = title_ch_paper
        books_conf.type_conf = type
        books_conf.date = date
        books_conf.pp = pp
        books_conf.save()

        return HttpResponseRedirect(reverse(conference_display))
    else:
        current_user=request.user
        score,empty_list = profile(current_user)
        return render(request,'website/conference.html',{
            'current_user': current_user,
            'date': current_date(),
            'mor_eve' : get_time_of_day(),
            'score':score,
            'empty_list':empty_list,
        })
    

'''
    Display all the data
'''

@login_required(login_url=login_view)
def patent_display(request):
    if request.method == 'POST':
        current_user = request.user
        field = request.POST['field']
        data = request.POST['q']
        user = 'user'
        filter_kwargs = {
            user:current_user,
            field:data
        }
        if current_user.employee_code == 'admin':
            filter_admin_kwargs = {
                field:data
            }
            if field == 'author_name':
                filter_patents = Patent.objects.filter(author_name__contains=data).all().order_by('-patent_year') 
            else:
                filter_patents = Patent.objects.filter(**filter_admin_kwargs).all().order_by('-patent_year') 
        else:
            if field == 'author_name':
                filter_patents = Patent.objects.filter(user=current_user,author_name__contains=data).all().order_by('-patent_year') 
            else:
                filter_patents = Patent.objects.filter(**filter_kwargs).all().order_by('-patent_year') 
        filter_patents_len = len(filter_patents)

        filter_patents_list = []
        f_count = 1
        for patent in filter_patents:
            filter_patents_list.append((f_count,patent))
            f_count+=1

        if current_user.employee_code == 'admin':
            df = pd.DataFrame(list(filter_patents.values()))
            filename = 'Filter_Patent_Download.xlsx'
            path = '.\website\csv_files'
            df.to_excel(os.path.join(path,filename))

        score,empty_list = profile(current_user)
        if filter_patents_len == 0:
            return render(request,'website/patent_display.html',{
            'filter_field':field,
            'filter_data':data,
            'message':'No Data Available',
            'current_user': current_user,
            'score':score,
            'empty_list':empty_list,
            })
        return render(request,'website/patent_display.html',{
            'filter_field':field,
            'filter_data':data,
            'filter_patents':filter_patents,
            'filter_patents_len':range(1,filter_patents_len+1),
            'filter_patents_list':filter_patents_list,
            'current_user': current_user,
            'score':score,
            'empty_list':empty_list,
    })
    else:
        current_user = request.user
        score,empty_list = profile(current_user)
        if current_user.employee_code == 'admin':
            patents = Patent.objects.all().order_by('-patent_year') 
            patents_len = len(patents)
            patents_list = []
            count = 1
            for patent in patents:
                patents_list.append((count,patent))
                count+=1


            df = pd.DataFrame(list(patents.values()))
            filename = 'Patent_Download.xlsx'
            path = '.\website\csv_files'
            df.to_excel(os.path.join(path,filename))

            
            
            return render(request,'website/patent_display.html',{
                'patents':patents,
                'patents_len':range(1,patents_len+1),
                'patents_list':patents_list,
                'current_user': current_user,
                'score':score,
                'empty_list':empty_list,
            })
        else:
            patents = Patent.objects.filter(user = current_user).all().order_by('-patent_year') 
            patents_len = len(patents)
            patents_list = []
            count = 1
            for patent in patents:
                patents_list.append((count,patent))
                count+=1

        
            return render(request,'website/patent_display.html',{
                'patents':patents,
                'patents_len':range(1,patents_len+1),
                'patents_list':patents_list,
                'current_user': current_user,
                'score':score,
            'empty_list':empty_list,
            })

@login_required(login_url=login_view)
def research_display(request):
    if request.method == 'POST':
        current_user = request.user
        field = request.POST['field']
        data = request.POST['q']
        user = 'user'
        filter_kwargs = {
            user:current_user,
            field:data
        }
        if current_user.employee_code == 'admin':
                filter_admin_kwargs = {
                    field:data
                }
                if field == 'author_name':
                    filter_papers = Paper_Publication.objects.filter(author_names__contains=data).all().order_by('-year_published')
                elif field == 'title':
                    filter_papers = Paper_Publication.objects.filter(title__contains=data).all().order_by('-year_published')
                else:
                    filter_papers = Paper_Publication.objects.filter(**filter_admin_kwargs).all().order_by('-year_published')
        else:
            if field == 'author_name':
                filter_papers = Paper_Publication.objects.filter(user=current_user,author_names__contains=data).all().order_by('-year_published')
            elif field == 'title':
                filter_papers = Paper_Publication.objects.filter(user=current_user,title__contains=data).all().order_by('-year_published')
            else:
                filter_papers = Paper_Publication.objects.filter(**filter_kwargs).all().order_by('-year_published')
        filter_papers_len = len(filter_papers)

        filter_papers_list = []
        f_count = 1
        for paper in filter_papers:
            filter_papers_list.append((f_count,paper))
            f_count+=1

        if current_user.employee_code == 'admin':
            df = pd.DataFrame(list(filter_papers.values()))
            filename = 'Filter_Research_Paper_Download.xlsx'
            path = '.\website\csv_files'
            df.to_excel(os.path.join(path,filename))

        score,empty_list = profile(current_user)

        if filter_papers_len == 0:
            return render(request,'website/research_display.html',{
            'filter_field':field,
            'filter_data':data,
            'message':'No Data Available',
            'current_user': current_user,
            'score':score,
            'empty_list':empty_list,
            })
        return render(request,'website/research_display.html',{
            'filter_field':field,
            'filter_data':data,
            'filter_papers':filter_papers,
            'filter_papers_len':range(1,filter_papers_len+1),
            'filter_papers_list':filter_papers_list,
            'current_user': current_user,
            'score':score,
            'empty_list':empty_list,
        })
    else:
        current_user = request.user
        score,empty_list = profile(current_user)
        if current_user.employee_code == 'admin':
            papers = Paper_Publication.objects.all().order_by('-year_published') 
            papers_list=[]
            count = 1
            for paper in papers:
                papers_list.append((count,paper))
                count+=1

            df = pd.DataFrame(list(papers.values()))
            filename = 'Research_Paper_Download.xlsx'
            path = '.\website\csv_files'
            df.to_excel(os.path.join(path,filename))


            return render(request,'website/research_display.html',{
                'papers':papers,
                'papers_list':papers_list,
                'current_user': current_user,
                'score':score,
            'empty_list':empty_list,
            })
        else:
            papers = Paper_Publication.objects.filter(user = current_user).all().order_by('-year_published') 
            papers_list=[]
            count = 1
            for paper in papers:
                papers_list.append((count,paper))
                count+=1
            return render(request,'website/research_display.html',{
                'papers':papers,
                'papers_list':papers_list,
                'current_user': current_user,
                'score':score,
            'empty_list':empty_list,
            })

@login_required(login_url=login_view)
def phd_display(request):
    if request.method == "POST":
        current_user = request.user
        field = request.POST['field']
        data = request.POST['q']
        user = 'user'
        filter_kwargs = {
            user:current_user,
            field:data
        }
        if current_user.employee_code == 'admin':
            filter_admin_kwargs = {
                field:data
            }
            if field == 'guide_names':
                filter_phds = PHD_Awarded.objects.filter(guide_names__contains=data).all().order_by('-registration_date')
            elif field == 'thesis_title':
                filter_phds = PHD_Awarded.objects.filter(thesis_title__contains=data).all().order_by('-registration_date')
            else:
                filter_phds = PHD_Awarded.objects.filter(**filter_admin_kwargs).all().order_by('-registration_date')
        else:
            if field == 'guide_names':
                filter_phds = PHD_Awarded.objects.filter(user=current_user,guide_names__contains=data).all().order_by('-registration_date')
            elif field == 'thesis_title':
                filter_phds = PHD_Awarded.objects.filter(user=current_user,thesis_title__contains=data).all().order_by('-registration_date')
            else:
                filter_phds = PHD_Awarded.objects.filter(**filter_kwargs).all().order_by('-registration_date')
        filter_phds_len = len(filter_phds)
        filter_phds_list = []
        f_count = 1
        for phd in filter_phds:
            filter_phds_list.append((f_count,phd))
            f_count+=1

        score,empty_list = profile(current_user)

        if current_user.employee_code == 'admin':
            df = pd.DataFrame(list(filter_phds.values()))
            filename = 'Filter_PhD_Download.xlsx'
            path = '.\website\csv_files'
            df.to_excel(os.path.join(path,filename))

        if filter_phds_len == 0:
            return render(request,'website/phd_display.html',{
            'filter_field':field,
            'filter_data':data,
            'message':'No Data Available',
            'current_user': current_user,
            'score':score,
            'empty_list':empty_list,
            })
        return render(request,'website/phd_display.html',{
            'filter_field':field,
            'filter_data':data,
            'filter_phds_list':filter_phds_list,
            'current_user': current_user,
            'score':score,
            'empty_list':empty_list,
        })
 
    else:
        current_user = request.user
        score,empty_list = profile(current_user)
        if current_user.employee_code == 'admin':
            phds = PHD_Awarded.objects.all().order_by('-registration_date') 
            phds_list=[]
            count = 1
            for phd in phds:
                phds_list.append((count,phd))
                count+=1

            if current_user.employee_code == 'admin':
                df = pd.DataFrame(list(phds.values()))
                filename = 'PhD_Download.xlsx'
                path = '.\website\csv_files'
                df.to_excel(os.path.join(path,filename))


            return render(request,'website/phd_display.html',{
                'phds_list':phds_list,
                'current_user': current_user,
                'score':score,
            'empty_list':empty_list,
            })
        else:
            phds = PHD_Awarded.objects.filter(user = current_user).all().order_by('-registration_date') 
            phds_list=[]
            count = 1
            for phd in phds:
                phds_list.append((count,phd))
                count+=1
            return render(request,'website/phd_display.html',{
                'phds_list':phds_list,
                'current_user': current_user,
                'score':score,
            'empty_list':empty_list,
            })
    
@login_required(login_url=login_view)
def award_display(request):
    if request.method == "POST":
        current_user = request.user
        field = request.POST['field']
        data = request.POST['q']
        user = 'user'
        filter_kwargs = {
            user:current_user,
            field:data
        }
        if current_user.employee_code == 'admin':
            filter_admin_kwargs = {
                field:data
            }
            filter_awards = Awards.objects.filter(**filter_admin_kwargs).all().order_by('-year_awarded')
        else:
            filter_awards = Awards.objects.filter(**filter_kwargs).all().order_by('-year_awarded')
        filter_awards_len = len(filter_awards)
        filter_awards_list = []
        f_count = 1
        for award in filter_awards:
            filter_awards_list.append((f_count,award))
            f_count+=1

        if current_user.employee_code == 'admin':
                df = pd.DataFrame(list(filter_awards.values()))
                filename = 'Filter_Awards_Download.xlsx'
                path = '.\website\csv_files'
                df.to_excel(os.path.join(path,filename))

        score,empty_list = profile(current_user)

        if filter_awards_len == 0:
            return render(request,'website/award_display.html',{
            'filter_field':field,
            'filter_data':data,
            'message':'No Data Available',
            'current_user': current_user,
            'score':score,
            'empty_list':empty_list,
            })
        return render(request,'website/award_display.html',{
            'filter_field':field,
            'filter_data':data,
            'filter_awards_list':filter_awards_list,
            'current_user': current_user,
            'score':score,
            'empty_list':empty_list,
        })

    else:
        current_user = request.user
        score,empty_list = profile(current_user)
        if current_user.employee_code == 'admin':
            awards = Awards.objects.all().order_by('-year_awarded') 
            awards_list=[]
            count = 1
            for award in awards:
                awards_list.append((count,award))
                count+=1

            if current_user.employee_code == 'admin':
                df = pd.DataFrame(list(awards.values()))
                filename = 'Awards_Download.xlsx'
                path = '.\website\csv_files'
                df.to_excel(os.path.join(path,filename))

            return render(request,'website/award_display.html',{
                'awards_list':awards_list,
                'current_user': current_user,
                'score':score,
            'empty_list':empty_list,
            })
        else:
            awards = Awards.objects.filter(user = current_user).all().order_by('-year_awarded') 
            awards_list=[]
            count = 1
            for award in awards:
                awards_list.append((count,award))
                count+=1
            return render(request,'website/award_display.html',{
                'awards_list':awards_list,
                'current_user': current_user,
                'score':score,
            'empty_list':empty_list,
            })
    
@login_required(login_url=login_view)
def books_display(request):
    if request.method == 'POST':
        current_user = request.user
        field = request.POST['field']
        data = request.POST['q']
        user = 'user'
        filter_kwargs = {
            user:current_user,
            field:data
        }
        filter_admin_kwargs = {
            field:data
        }
        if current_user.employee_code == 'admin':
            if field == 'authors':
                filter_books = Books.objects.filter(authors__contains=data).all().order_by('-year_published')
            elif field == 'title':
                filter_books = Books.objects.filter(title__contains=data).all().order_by('-year_published')
            else:
                filter_books = Books.objects.filter(**filter_admin_kwargs).all().order_by('-year_published')
        else:
            if field == 'authors':
                filter_books = Books.objects.filter(user=current_user,authors__contains=data).all().order_by('-year_published')
            elif field == 'title':
                filter_books = Books.objects.filter(user=current_user,title__contains=data).all().order_by('-year_published')
            else:
                filter_books = Books.objects.filter(**filter_kwargs).all().order_by('-year_published')
        filter_books_len = len(filter_books)
        filter_books_list = []
        f_count = 1
        for book in filter_books:
            filter_books_list.append((f_count,book))
            f_count+=1

        if current_user.employee_code == 'admin':
                df = pd.DataFrame(list(filter_books.values()))
                filename = 'Filter_Books_Download.xlsx'
                path = '.\website\csv_files'
                df.to_excel(os.path.join(path,filename))

        score,empty_list = profile(current_user)
        if filter_books_len == 0:
            return render(request,'website/books_display.html',{
            'filter_field':field,
            'filter_data':data,
            'message':'No Data Available',
            'current_user': current_user,
            'score':score,
            'empty_list':empty_list,
            })
        return render(request,'website/books_display.html',{
            'filter_field':field,
            'filter_data':data,
            'filter_books_list':filter_books_list,
            'current_user': current_user,
            'score':score,
            'empty_list':empty_list,
        })
    else:
        current_user = request.user
        score,empty_list = profile(current_user)
        if current_user.employee_code == 'admin':
            books = Books.objects.all().order_by('-year_published') 
            books_list=[]
            count = 1
            for book in books:
                books_list.append((count,book))
                count+=1

            if current_user.employee_code == 'admin':
                df = pd.DataFrame(list(books.values()))
                filename = 'Books_Download.xlsx'
                path = '.\website\csv_files'
                df.to_excel(os.path.join(path,filename))

            return render(request,'website/books_display.html',{
                'books_list':books_list,
                'current_user': current_user,
                'score':score,
            'empty_list':empty_list,
            })
        else:
            books = Books.objects.filter(user = current_user).all().order_by('-year_published') 
            books_list=[]
            count = 1
            for book in books:
                books_list.append((count,book))
                count+=1
            return render(request,'website/books_display.html',{
                'books_list':books_list,
                'current_user': current_user,
                'score':score,
            'empty_list':empty_list,
            })
        
@login_required(login_url=login_view)
def conference_display(request):
    if request.method == "POST":
        current_user = request.user
        field = request.POST['field']
        data = request.POST['q']
        user = 'user'
        filter_kwargs = {
            user:current_user,
            field:data
        }
        filter_admin_kwargs = {
            user:current_user,
            field:data
        }
        if current_user.employee_code == 'admin':
            if field == 'authors':
                filter_conferences = Books_Conference.objects.filter(authors__contains=data).all().order_by('-date')
            elif field == 'title_chap_paper':
                filter_conferences = Books_Conference.objects.filter(title_chap_paper__contains=data).all().order_by('-date')
            elif field == 'title_book_conf':
                filter_conferences = Books_Conference.objects.filter(title_book_conf__contains=data).all().order_by('-date')
            else:
                filter_conferences = Books_Conference.objects.filter(**filter_admin_kwargs).all().order_by('-date')
        else:
            if field == 'authors':
                filter_conferences = Books_Conference.objects.filter(user=current_user,authors__contains=data).all().order_by('-date')
            elif field == 'title_chap_paper':
                filter_conferences = Books_Conference.objects.filter(user=current_user,title_chap_paper__contains=data).all().order_by('-date')
            elif field == 'title_book_conf':
                filter_conferences = Books_Conference.objects.filter(user=current_user,title_book_conf__contains=data).all().order_by('-date')
            else:
                filter_conferences = Books_Conference.objects.filter(**filter_kwargs).all().order_by('-date')
        filter_conferences_len = len(filter_conferences)
        filter_conferences_list = []
        f_count = 1
        for conference in filter_conferences:
            filter_conferences_list.append((f_count,conference))
            f_count+=1

        if current_user.employee_code == 'admin':
                df = pd.DataFrame(list(filter_conferences.values()))
                filename = 'Filter_Conference_Download.xlsx'
                path = '.\website\csv_files'
                df.to_excel(os.path.join(path,filename))

        score,empty_list = profile(current_user)
        if filter_conferences_len == 0:
            return render(request,'website/conference_display.html',{
            'filter_field':field,
            'filter_data':data,
            'message':'No Data Available',
            'current_user': current_user,
            'score':score,
            'empty_list':empty_list,
            })
        return render(request,'website/conference_display.html',{
            'filter_field':field,
            'filter_data':data,
            'filter_conferences_list':filter_conferences_list,
            'current_user': current_user,
            'score':score,
            'empty_list':empty_list,
        })
    else:
        current_user = request.user
        score,empty_list = profile(current_user)
        if current_user.employee_code == 'admin':
            conferences = Books_Conference.objects.all().order_by('-date') 
            conferences_list=[]
            count = 1
            for conference in conferences:
                conferences_list.append((count,conference))
                count+=1

            if current_user.employee_code == 'admin':
                df = pd.DataFrame(list(conferences.values()))
                filename = 'Conference_Download.xlsx'
                path = '.\website\csv_files'
                df.to_excel(os.path.join(path,filename))

            return render(request,'website/conference_display.html',{
                'conferences_list':conferences_list,
                'current_user': current_user,
                'score':score,
            'empty_list':empty_list,
            })
        else:
            conferences = Books_Conference.objects.filter(user = current_user).all().order_by('-date') 
            conferences_list=[]
            count = 1
            for conference in conferences:
                conferences_list.append((count,conference))
                count+=1
            return render(request,'website/conference_display.html',{
                'conferences_list':conferences_list,
                'current_user': current_user,
                'score':score,
            'empty_list':empty_list,
            })
    
'''
    Edit the Info
'''
@login_required(login_url=login_view)
def edit_patent(request,id):
    if request.method == 'POST':
        patent_number = request.POST["patent_number"]
        patent_title = request.POST["patent_title"]
        year_awarded = request.POST["year_awarded"]
        author_name = request.POST['author_name']
        category = request.POST['category']

        patent = Patent.objects.filter(user=request.user).get(id=id)
        patent.author_name = author_name
        patent.patent_number = patent_number
        patent.patent_title = patent_title
        patent.patent_year = year_awarded
        patent.category = category
        patent.save()

        messages.success(request, 'Patent Edited Successfully')

        return HttpResponseRedirect(reverse(patent_display))
    else:
        patent = Patent.objects.filter(user=request.user).get(id=id)
        score,empty_list = profile(request.user)
        return render(request,'website/patent.html',{
            'edit_patent':patent,
            'current_user': request.user,
            'mor_eve' : get_time_of_day(),
            'date': current_date(),
            'score':score,
            'empty_list':empty_list,
        })
    
@login_required(login_url=login_view)
def edit_phd(request,id):
    if request.method == 'POST':
        department = request.POST["department"]
        guide_names = request.POST["guide_names"]
        thesis_title = request.POST["thesis_title"]
        registration_date = request.POST["registration_date"]
        award_date = request.POST["award_date"]
        scholor_name = request.POST['scholor_name']

        phd = PHD_Awarded.objects.filter(user=request.user).get(id=id)
        phd.user = request.user
        phd.scholor_name = scholor_name
        phd.department = department
        phd.guide_names = guide_names
        phd.thesis_title = thesis_title
        phd.award_date = award_date
        phd.registration_date = registration_date
        phd.save()

        messages.success(request, 'Ph.D Edited Successfully')

        return HttpResponseRedirect(reverse(phd_display))
    else:
        phd = PHD_Awarded.objects.filter(user=request.user).get(id=id)
        score,empty_list = profile(request.user)
        return render(request,'website/phd.html',{
            'edit_phd':phd,
            'current_user': request.user,
            'mor_eve' : get_time_of_day(),
            'date': current_date(),
            'score':score,
            'empty_list':empty_list,
        })

@login_required(login_url=login_view) 
def edit_research(request,id):
    if request.method == "POST":
        title = request.POST["title"]
        author_names = request.POST["author_names"]
        journal_name = request.POST["journal_name"]
        journal_url = request.POST["journal_url"]
        issn = request.POST["issn"]
        publisher = request.POST["publisher"]
        month_published = request.POST["month_published"]
        year_published = request.POST["year_published"]
        volume_number = request.POST["volume_number"]
        issue_number = request.POST["issue_number"]
        pp = request.POST["pp"]
        doi = request.POST["doi"]
        ugc_core = request.POST["ugc_core"]
        scopus = request.POST["scopus"]
        sci_scie_esci = request.POST["sci_scie_esci"]
        if sci_scie_esci != 'None':
            impact_factor = request.POST["impact_factor"]

        paper = Paper_Publication.objects.filter(user=request.user).get(id=id)
        paper.user = request.user
        paper.title = title
        paper.author_names = author_names
        paper.journal_name = journal_name
        paper.journal_website = journal_url
        paper.issn = issn
        paper.publisher = publisher
        paper.month_published = month_published
        paper.year_published = year_published
        paper.volume_number = volume_number
        paper.issue_number = issue_number
        paper.pp = pp
        paper.doi = doi
        paper.ugc_core = ugc_core
        paper.scopus = scopus
        paper.sci_scie_esci = sci_scie_esci
        if sci_scie_esci != 'None':
            paper.impact_factor = impact_factor
        paper.save()

        messages.success(request, 'Research Paper Edited Successfully')

        return HttpResponseRedirect(reverse(research_display))
    else:
        research = Paper_Publication.objects.filter(user=request.user).get(id=id)
        score,empty_list = profile(request.user)
        return render(request,'website/research.html',{
            'edit_research':research,
            'current_user': request.user,
            'mor_eve' : get_time_of_day(),
            'date': current_date(),
            'score':score,
            'empty_list':empty_list,
        })
    
@login_required(login_url=login_view)
def edit_award(request,id):
    if request.method == "POST":
        activity = request.POST["activity"]
        award_name = request.POST["award_name"]
        authority_name = request.POST["authority_name"]
        year_awarded = request.POST["year_awarded"]
        scholor_name = request.POST['scholor_name']
        level = request.POST['level']

        award = Awards.objects.filter(user=request.user).get(id=id)
        award.user = request.user
        award.scholor_name = scholor_name
        award.activity = activity
        award.award_name = award_name
        award.authority_name = authority_name
        award.year_awarded = year_awarded
        award.level = level
        award.save()

        messages.success(request, 'Award Edited Successfully')

        return HttpResponseRedirect(reverse(award_display))
    else:
        award = Awards.objects.filter(user=request.user).get(id=id)
        score,empty_list = profile(request.user)
        return render(request,'website/award.html',{
            'edit_award':award,
            'current_user': request.user,
            'mor_eve' : get_time_of_day(),
            'date': current_date(),
            'score':score,
            'empty_list':empty_list,
        })

@login_required(login_url=login_view)
def edit_book(request,id):
    if request.method == "POST":
        author_name = request.POST["author_name"]
        book_title = request.POST["book_title"]
        publisher = request.POST["publisher"]
        isbn = request.POST["isbn"]
        year_published = request.POST["year_published"]
        affiliate_uni = request.POST['affiliate_uni']

        books = Books.objects.filter(user=request.user).get(id=id)
        books.user = request.user
        books.authors = author_name
        books.title = book_title
        books.publisher = publisher
        books.isbn = isbn
        books.year_published = year_published
        books.affiliating_institute = affiliate_uni
        books.save()

        messages.success(request, 'Book Edited Successfully')

        return HttpResponseRedirect(reverse(books_display))
    else:
        book = Books.objects.filter(user=request.user).get(id=id)
        score,empty_list = profile(request.user)
        return render(request,'website/books.html',{
            'edit_book':book,
            'current_user': request.user,
            'mor_eve' : get_time_of_day(),
            'date': current_date(),
            'score':score,
            'empty_list':empty_list,
        })
    
@login_required(login_url=login_view)
def edit_conference(request,id):
    if request.method == "POST":
        author_name = request.POST["author_name"]
        category = request.POST["category"]
        type = request.POST["type"]
        publisher = request.POST["publisher"]
        date = request.POST["date"]
        title_ch_paper = request.POST['title_ch_paper']
        title_book_conf = request.POST['title_book_conf']
        isbn = request.POST['isbn']
        pp = request.POST['pp']

        books_conf = Books_Conference.objects.filter(user=request.user).get(id=id)
        books_conf.user = request.user
        books_conf.authors = author_name
        books_conf.category = category
        books_conf.publisher = publisher
        books_conf.isbn = isbn
        books_conf.title_book_conf = title_book_conf
        books_conf.title_chap_paper = title_ch_paper
        books_conf.type_conf = type
        books_conf.date = date
        books_conf.pp = pp
        books_conf.save()

        messages.success(request, 'Conference Edited Successfully')

        return HttpResponseRedirect(reverse(conference_display))
    else:
        conference = Books_Conference.objects.filter(user=request.user).get(id=id)
        score,empty_list = profile(request.user)
        return render(request,'website/conference.html',{
            'edit_conference':conference,
            'current_user': request.user,
            'mor_eve' : get_time_of_day(),
            'date': current_date(),
            'score':score,
            'empty_list':empty_list,
        })
    
   
'''
    Delete the Info
'''
@login_required(login_url=login_view)
def delete_patent(request,id):
    patent = Patent.objects.filter(user=request.user).get(id=id)
    patent.delete()
    messages.error(request, f'{patent.patent_title} Removed')
    return HttpResponseRedirect(reverse(patent_display))

@login_required(login_url=login_view)
def delete_phd(request,id):
    phd = PHD_Awarded.objects.filter(user=request.user).get(id=id)
    phd.delete()
    messages.error(request, f'{phd.scholor_name} Removed')
    return HttpResponseRedirect(reverse(phd_display))

@login_required(login_url=login_view)
def delete_research(request,id):
    research = Paper_Publication.objects.filter(user=request.user).get(id=id)
    research.delete()
    messages.error(request, f'{research.title} Removed')
    return HttpResponseRedirect(reverse(research_display))

@login_required(login_url=login_view)
def delete_award(request,id):
    award = Awards.objects.filter(user=request.user).get(id=id)
    award.delete()
    messages.error(request, f'{award.award_name} Removed')
    return HttpResponseRedirect(reverse(award_display))

@login_required(login_url=login_view)
def delete_book(request,id):
    book = Books.objects.filter(user=request.user).get(id=id)
    book.delete()
    messages.error(request, f'{book.title} Removed')
    return HttpResponseRedirect(reverse(books_display))

@login_required(login_url=login_view)
def delete_conference(request,id):
    conference = Books_Conference.objects.filter(user=request.user).get(id=id)
    conference.delete()
    messages.error(request, f'{conference.title_book_conf} Removed')
    return HttpResponseRedirect(reverse(conference_display))


'''
    CSV Download FILES
'''

@login_required(login_url=login_view)
def patent_download(request):
    if request.method=="GET" and 'patent' in request.GET:
        filename = 'Patent_Download.xlsx'
        path = '.\website\csv_files'
        df = pd.read_excel(os.path.join(path,filename))
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="Patents_CSV_Download.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['Index','Author Name', 'Patent Number', 'Patent Title', 'Category','Patent Year'])
        for index, row in df.iterrows():
            writer.writerow([index+1,row['author_name'], row['patent_number'], row['patent_title'], row['category'],str(row['patent_year']).replace(' 00:00:00','')])    

        return response
    elif request.method == "GET" and 'filter_patent' in request.GET:
        filename = 'Filter_Patent_Download.xlsx'
        path = '.\website\csv_files'
        df = pd.read_excel(os.path.join(path,filename))
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="Filter_Patents_CSV_Download.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['Index','Author Name', 'Patent Number', 'Patent Title', 'Category','Patent Year'])
        for index, row in df.iterrows():
            writer.writerow([index+1,row['author_name'], row['patent_number'], row['patent_title'], row['category'],str(row['patent_year']).replace(' 00:00:00','')])    

        return response
    
@login_required(login_url=login_view)
def research_download(request):
    if request.method =="GET" and 'research' in request.GET:
        filename = 'Research_Paper_Download.xlsx'
        path = '.\website\csv_files'
        df = pd.read_excel(os.path.join(path,filename))
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="Research_Paper_CSV_Download.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['Index', 'Title', 'Author Name(s)', 'Journal Name', 'Journal Website', 'ISSN','Publisher', 'Month Published', 'Year Published', 'Volume Number', 'Issue Number', 'PP', 'D.O.I', 'UGC Core', 'Scopus', 'SCI/SCIE/ESCI', 'Impact Factor'])
        for index, row in df.iterrows():
            writer.writerow([index+1,row['scholor_name'], row['department'], row['guide_names'], row['thesis_title'], row['registration_date'], row['award_date'], row['month_published'], row['year_published'], row['volume_number'], row['issue_number'], row['pp'], row['doi'], row['ugc_core'], row['scopus'], row['sci_scie_esci'], row['impact_factor']])    

        return response
    elif request.method == "GET" and 'filter_research' in request.GET:
        filename = 'Filter_Research_Paper_Download.xlsx'
        path = '.\website\csv_files'
        df = pd.read_excel(os.path.join(path,filename))
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="Filter_Research_Paper_CSV_Download.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['Index', 'Title', 'Author Name(s)', 'Journal Name', 'Journal Website', 'ISSN','Publisher', 'Month Published', 'Year Published', 'Volume Number', 'Issue Number', 'PP', 'D.O.I', 'UGC Core', 'Scopus', 'SCI/SCIE/ESCI', 'Impact Factor'])
        for index, row in df.iterrows():
            writer.writerow([index+1,row['title'], row['author_names'], row['journal_name'], row['journal_website'], row['issn'], row['publisher'], row['month_published'], row['year_published'], row['volume_number'], row['issue_number'], row['pp'], row['doi'], row['ugc_core'], row['scopus'], row['sci_scie_esci'], row['impact_factor']])    

        return response

@login_required(login_url=login_view)
def phd_download(request):
    if request.method =="GET" and 'phd' in request.GET:
        filename = 'PhD_Download.xlsx'
        path = '.\website\csv_files'
        df = pd.read_excel(os.path.join(path,filename))
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="Phd_CSV_Download.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['Index', 'Scholor Name', 'Department', 'Guide Name(s)', 'Thesis Title', 'Registration Date', 'Award Date'])
        for index, row in df.iterrows():
            writer.writerow([index+1,row['scholor_name'], row['department'], row['guide_names'], row['thesis_title'], row['registration_date'], row['award_date']])    

        return response
    elif request.method == "GET" and 'filter_phd' in request.GET:
        filename = 'Filter_PhD_Download.xlsx'
        path = '.\website\csv_files'
        df = pd.read_excel(os.path.join(path,filename))
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="Filter_PhD_CSV_Download.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['Index', 'Scholor Name', 'Department', 'Guide Name(s)', 'Thesis Title', 'Registration Date', 'Award Date'])
        for index, row in df.iterrows():
            writer.writerow([index+1,row['scholor_name'], row['department'], row['guide_names'], row['thesis_title'], row['registration_date'], row['award_date']]) 

        return response
    
@login_required(login_url=login_view)
def award_download(request):
    if request.method =="GET" and 'award' in request.GET:
        filename = 'Awards_Download.xlsx'
        path = '.\website\csv_files'
        df = pd.read_excel(os.path.join(path,filename))
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="Awards_CSV_Download.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['Index', 'Scholor Name', 'Activity', 'Activity', 'Award Name', 'Authority Name', 'Year Awarded','Level'])
        for index, row in df.iterrows():
            writer.writerow([index+1,row['scholor_name'], row['activity'], row['award_name'], row['authority_name'], row['year_awarded'], row['level']])    

        return response
    elif request.method == "GET" and 'filter_award' in request.GET:
        filename = 'Filter_Awards_Download.xlsx'
        path = '.\website\csv_files'
        df = pd.read_excel(os.path.join(path,filename))
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="Filter_Awards_CSV_Download.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['Index', 'Scholor Name', 'Activity', 'Activity', 'Award Name', 'Authority Name', 'Year Awarded','Level'])
        for index, row in df.iterrows():
            writer.writerow([index+1,row['scholor_name'], row['activity'], row['award_name'], row['authority_name'], row['year_awarded'], row['level']])    

        return response

@login_required(login_url=login_view)   
def books_download(request):
    if request.method =="GET" and 'books' in request.GET:
        filename = 'Books_Download.xlsx'
        path = '.\website\csv_files'
        df = pd.read_excel(os.path.join(path,filename))
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="Books_CSV_Download.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['Index', 'Author Name(s)', 'Title', 'Publisher', 'ISBN', 'Year Published', 'Affiliating Institute'])
        for index, row in df.iterrows():
            writer.writerow([index+1,row['authors'], row['title'], row['publisher'], row['isbn'], row['year_published'], row['affiliating_institute']])    

        return response
    elif request.method == "GET" and 'filter_books' in request.GET:
        filename = 'Filter_Books_Download.xlsx'
        path = '.\website\csv_files'
        df = pd.read_excel(os.path.join(path,filename))
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="Filter_Books_CSV_Download.csv"'},
        )
        
        writer = csv.writer(response)
        writer.writerow(['Index', 'Author Name(s)', 'Title', 'Publisher', 'ISBN', 'Year Published', 'Affiliating Institute'])
        for index, row in df.iterrows():
            writer.writerow([index+1,row['authors'], row['title'], row['publisher'], row['isbn'], row['year_published'], row['affiliating_institute']])    

        return response

@login_required(login_url=login_view)   
def conference_download(request):
    if request.method =="GET" and 'conference' in request.GET:
        filename = 'Conference_Download.xlsx'
        path = '.\website\csv_files'
        df = pd.read_excel(os.path.join(path,filename))
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="Conference_Proceedings_CSV_Download.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['Index', 'Author Name(s)', 'Category', 'Title of Chapter/Paper', 'Title of Book/Conference', 'Type of Conference', 'Date', 'ISBN', 'Publisher', 'PP'])
        for index, row in df.iterrows():
            writer.writerow([index+1,row['authors'], row['category'], row['title_chap_paper'], row['title_book_conf'], row['type_conf'], row['date'], row['isbn'], row['publisher'], row['pp']])    

        return response
    elif request.method == "GET" and 'filter_conference' in request.GET:
        filename = 'Filter_Conference_Download.xlsx'
        path = '.\website\csv_files'
        df = pd.read_excel(os.path.join(path,filename))
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="Filter_Conference_Proceedings_CSV_Download.csv"'},
        )
        
        writer = csv.writer(response)
        writer.writerow(['Index', 'Author Name(s)', 'Category', 'Title of Chapter/Paper', 'Title of Book/Conference', 'Type of Conference', 'Date', 'ISBN', 'Publisher', 'PP'])
        for index, row in df.iterrows():
            writer.writerow([index+1,row['authors'], row['category'], row['title_chap_paper'], row['title_book_conf'], row['type_conf'], row['date'], row['isbn'], row['publisher'], row['pp']])    
        return response
